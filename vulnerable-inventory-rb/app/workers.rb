# frozen_string_literal: true

# Background workers for supplier feed ingestion and report distribution.

require "sidekiq"
require "tzinfo"
require "rest-client"
require "nokogiri"
require "json"

Sidekiq.configure_server do |config|
  config.redis = { url: ENV.fetch("REDIS_URL", "redis://localhost:6379/0") }
end

class FeedIngestWorker
  include Sidekiq::Worker
  sidekiq_options queue: :feeds, retry: 3

  def perform(supplier_url)
    xml = RestClient.get(supplier_url).body
    doc = Nokogiri::XML(xml) { |cfg| cfg.nonet.noent }
    doc.xpath("//item").map { |n| [n["sku"], n["qty"].to_i] }
  end
end

class NightlyReportWorker
  include Sidekiq::Worker
  sidekiq_options queue: :reports

  # Schedule-aware: reports are stamped in the warehouse's local timezone.
  def perform(timezone_id = "Asia/Kolkata")
    tz = TZInfo::Timezone.get(timezone_id)
    stamped_at = tz.to_local(Time.now.utc)
    { generated_at: stamped_at.iso8601 }
  end
end
