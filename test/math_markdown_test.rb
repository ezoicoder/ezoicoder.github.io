# frozen_string_literal: true

require "kramdown"
require "open3"
require "tempfile"
require_relative "../_plugins/conventional_math_gfm"

OPTIONS = {
  input: "ConventionalMathGFM",
  math_engine: :mathjax
}.freeze

def render(source)
  Kramdown::Document.new(source, **OPTIONS).to_html
end

def assert(condition, message)
  raise message unless condition
end

inline = render('Before $x_{n-2}$ after.')
assert(
  inline == "<p>Before \\(x_{n-2}\\) after.</p>\n",
  "single-dollar math did not render inline"
)

multiple = render(
  'The $\mathcal{G}_{L,n}$ distribution and $x_{n-2}$ value.'
)
assert(
  multiple.include?('\(\mathcal{G}_{L,n}\)') &&
    multiple.include?('\(x_{n-2}\)') &&
    !multiple.include?("<em>"),
  "underscores collided with Markdown emphasis"
)

display = render("Before.\n\n$$\nx_{n-2}\n$$\n\nAfter.")
assert(
  display.include?("\\[x_{n-2}\\]") &&
    !display.include?("<p>\\[x_{n-2}\\]</p>"),
  "double-dollar math did not render as a display block"
)

code = render('Write `$x_i$` for inline math.')
assert(
  code.include?('<code>$x_i$</code>'),
  "code-span math was parsed"
)

escaped = render('The price is \$5.')
assert(
  escaped.include?("The price is $5."),
  "escaped dollar did not remain literal"
)

checker = File.expand_path("../tools/check_kramdown_math.rb", __dir__)

Tempfile.create(["wrapped-inline-math", ".md"]) do |file|
  file.write("Before $x=\ny$ after.\n")
  file.flush
  _stdout, stderr, status = Open3.capture3("ruby", checker, file.path)
  assert(
    !status.success? && stderr.include?("unbalanced inline-math delimiter"),
    "wrapped inline math was not rejected by the checker"
  )
end

Tempfile.create(["ignored-dollar-contexts", ".md"]) do |file|
  file.write(<<~MARKDOWN)
    Before $x=y$ after and the price is \\$5.

    Write `$x=` as literal code.

    <!--
    $commented=
    math$
    -->

    ```text
    $code=
    block$
    ```
  MARKDOWN
  file.flush
  _stdout, stderr, status = Open3.capture3("ruby", checker, file.path)
  assert(status.success?, "checker rejected ignored dollar context: #{stderr}")
end

puts "Math Markdown parser tests passed."
