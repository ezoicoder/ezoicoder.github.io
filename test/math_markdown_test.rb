# frozen_string_literal: true

require "kramdown"
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

puts "Math Markdown parser tests passed."
