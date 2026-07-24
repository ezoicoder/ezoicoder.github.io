# frozen_string_literal: true

require "kramdown-parser-gfm"

module Kramdown
  module Parser
    # GFM with conventional TeX delimiters:
    #   $...$   inline math
    #   $$...$$ display math (handled by Kramdown's block-math parser)
    class ConventionalMathGFM < GFM
      INLINE_MATH_START =
        /(?<!\\|\$)\$(?!\$|\s)([^\n]*?\S)(?<!\\|\$)\$(?!\$)/

      def initialize(source, options)
        super
        index = @span_parsers.index(:inline_math)
        @span_parsers[index] = :conventional_inline_math
      end

      def parse_conventional_inline_math
        start_line_number = @src.current_line_number
        @src.pos += @src.matched_size
        @tree.children << Element.new(
          :math,
          @src[1],
          nil,
          category: :span,
          location: start_line_number
        )
      end

      define_parser(
        :conventional_inline_math,
        INLINE_MATH_START,
        "\\$"
      )
    end
  end
end
