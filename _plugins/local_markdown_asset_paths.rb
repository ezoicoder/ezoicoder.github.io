# frozen_string_literal: true

module LocalMarkdownAssetPaths
  ASSET_ATTRIBUTE = /(?<attribute>\b(?:src|href))=(?<quote>["'])\.\.\/assets\//

  class RelativeUrlFilter
    include Jekyll::Filters::URLFilters

    def initialize(site)
      @context = Liquid::Context.new({}, {}, { site: site })
    end
  end

  def self.rewrite(html, site)
    asset_root = RelativeUrlFilter.new(site).relative_url("/assets/")

    html.gsub(ASSET_ATTRIBUTE) do
      "#{Regexp.last_match[:attribute]}=#{Regexp.last_match[:quote]}#{asset_root}"
    end
  end
end

Jekyll::Hooks.register :posts, :post_render do |post|
  post.output = LocalMarkdownAssetPaths.rewrite(post.output, post.site)
end
