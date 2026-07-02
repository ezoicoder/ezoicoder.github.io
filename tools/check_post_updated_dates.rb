#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"

staged = false
if ARGV.first == "--staged"
  staged = true
  ARGV.shift
end

def command_output(*args)
  IO.popen(args, &:read)
end

def git_object_exists?(object)
  system("git", "cat-file", "-e", object, out: File::NULL, err: File::NULL)
end

def frontmatter_and_body(source)
  match = source.match(/\A---\n(.*?)\n---\n/m)
  return [nil, source] unless match

  [match[1], source[match.end(0)..] || ""]
end

def updated_date(frontmatter)
  return nil unless frontmatter

  line = frontmatter.lines.find { |candidate| candidate.match?(/\Aupdated:\s*\d{4}-\d{2}-\d{2}\s*\z/) }
  return nil unless line

  Date.iso8601(line[/\d{4}-\d{2}-\d{2}/])
rescue Date::Error
  nil
end

paths =
  if ARGV.empty?
    if staged
      command_output("git", "diff", "--cached", "--name-only", "--diff-filter=ACMRT", "-z", "--", "_posts/*.md")
        .split("\0")
        .reject(&:empty?)
    else
      command_output("git", "diff", "--name-only", "--diff-filter=ACMRT", "-z", "--", "_posts/*.md")
        .split("\0")
        .reject(&:empty?)
    end
  else
    ARGV
  end

today = Date.today
bad = []

paths.each do |path|
  source =
    if staged
      command_output("git", "show", ":#{path}")
    else
      File.read(path)
    end

  frontmatter, body = frontmatter_and_body(source)

  old_object = "HEAD:#{path}"
  old_body =
    if git_object_exists?(old_object)
      old_source = command_output("git", "show", old_object)
      frontmatter_and_body(old_source)[1]
    end

  body_changed = old_body != body
  next unless body_changed

  updated = updated_date(frontmatter)
  bad << [path, updated] if updated.nil? || updated < today
end

if bad.empty?
  checked = staged ? "staged blog posts" : "blog posts"
  puts "Post updated dates are current for #{checked}."
  exit 0
end

warn "Blog post body changed without a current updated date:"
bad.each do |path, updated|
  value = updated ? updated.iso8601 : "missing or invalid"
  warn "#{path}: updated is #{value}; set it to at least #{today.iso8601}"
end
exit 1
