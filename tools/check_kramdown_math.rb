#!/usr/bin/env ruby
# frozen_string_literal: true

require "bundler/setup"
require "kramdown"
require_relative "../_plugins/conventional_math_gfm"

staged = false
if ARGV.first == "--staged"
  staged = true
  ARGV.shift
end

paths = ARGV
if paths.empty?
  paths =
    if staged
      `git diff --cached --name-only --diff-filter=ACMRT -- '*.md'`
        .lines
        .map(&:chomp)
    else
      Dir.glob("**/*.md", File::FNM_DOTMATCH).reject do |path|
        path.start_with?("_site/", "vendor/", ".bundle/", ".git/")
      end
    end
end

bad = []

paths.each do |path|
  source =
    if staged
      IO.popen(["git", "show", ":#{path}"], &:read)
    else
      File.read(path)
    end

  next if source.empty?

  html = Kramdown::Document.new(
    source,
    input: "ConventionalMathGFM",
    math_engine: :mathjax
  ).to_html

  html.lines.each_with_index do |line, index|
    if path.start_with?("_posts/") &&
       line.include?("$$") &&
       !line.include?("<code>")
      bad << [path, index + 1, line.strip]
      next
    end

    next unless line.include?("<em>")

    math_like =
      line.include?("$") ||
      line.include?("\\(") ||
      line.include?("\\[") ||
      line.include?("\\math") ||
      line.include?("\\cdot") ||
      line.include?("\\in ") ||
      line.include?("\\to")

    bad << [path, index + 1, line.strip] if math_like
  end
end

if bad.empty?
  checked = staged ? "staged Markdown" : "Markdown"
  puts "No Kramdown math/emphasis collisions found in #{checked}."
  exit 0
end

warn "Possible Kramdown math problems:"
bad.each do |path, line, text|
  warn "#{path}:#{line}: #{text}"
end
exit 1
