# frozen_string_literal: true

module FeedImageFilter
  DEFAULT_MAX_WIDTH = 720

  def feed_image_attrs(input, max_width = DEFAULT_MAX_WIDTH)
    input.to_s.gsub(/<img\b[^>]*>/i) do |tag|
      rewrite_feed_image_tag(tag, max_width.to_i)
    end
  end

  private

  def rewrite_feed_image_tag(tag, max_width)
    self_closing = tag.match?(%r{/\s*>\z})
    attr_text = tag.sub(/\A<img\b/i, '').sub(%r{/\s*>\z|>\z}, '')

    attrs = []
    attr_text.scan(/([:\w-]+)(?:\s*=\s*(".*?"|'.*?'|[^\s"'=<>`]+))?/m) do |name, raw_value|
      attrs << [name, raw_value && unquote_attr(raw_value)]
    end

    attr_hash = attrs.to_h
    width = integer_attr(attr_hash['width'])
    height = integer_attr(attr_hash['height'])

    if width && width > max_width
      attr_hash['width'] = max_width.to_s
      attr_hash['height'] = ((height * max_width.to_f) / width).round.to_s if height
    end

    attr_hash['style'] = responsive_feed_style(attr_hash['style'])

    rendered_attrs = attrs.map do |name, value|
      next unless attr_hash.key?(name)

      value = attr_hash[name]
      value.nil? ? name : %(#{name}="#{escape_attr(value)}")
    end.compact

    unless attrs.any? { |name, _| name == 'style' }
      rendered_attrs << %(style="#{escape_attr(attr_hash['style'])}")
    end

    suffix = self_closing ? ' />' : '>'
    "<img #{rendered_attrs.join(' ')}#{suffix}"
  end

  def integer_attr(value)
    value.to_s.match?(/\A\d+\z/) ? value.to_i : nil
  end

  def responsive_feed_style(style)
    declarations = style.to_s.strip
    declarations += ';' unless declarations.empty? || declarations.end_with?(';')
    declarations += ' max-width: 100%;' unless declarations.match?(/(^|;)\s*max-width\s*:/i)
    declarations += ' height: auto;' unless declarations.match?(/(^|;)\s*height\s*:/i)
    declarations.strip
  end

  def unquote_attr(value)
    value.start_with?('"', "'") ? value[1...-1] : value
  end

  def escape_attr(value)
    value.to_s.gsub('"', '&quot;')
  end
end

Liquid::Template.register_filter(FeedImageFilter)
