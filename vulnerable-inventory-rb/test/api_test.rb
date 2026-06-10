# frozen_string_literal: true

# Smoke tests — give your remediation agent a validation gate to run after
# upgrading dependencies (`bundle exec rake test`).

ENV["DB_PATH"] = ":memory:"

require "minitest/autorun"
require "rack/test"
require_relative "../app/api"

class InventoryAPITest < Minitest::Test
  include Rack::Test::Methods

  def app
    InventoryAPI
  end

  def setup
    Product.delete_all
  end

  def test_health
    get "/health"
    assert_equal 200, last_response.status
    assert_equal "ok", JSON.parse(last_response.body)["status"]
  end

  def test_create_and_list_product
    post "/products",
         JSON.generate(sku: "TEST-001", name: "Test Widget", quantity: 5),
         "CONTENT_TYPE" => "application/json"
    assert_equal 201, last_response.status

    get "/products"
    skus = JSON.parse(last_response.body).map { |p| p["sku"] }
    assert_includes skus, "TEST-001"
  end

  def test_description_is_sanitized
    post "/products",
         JSON.generate(
           sku: "TEST-002",
           name: "Widget",
           description: "<b>nice</b><script>alert(1)</script>"
         ),
         "CONTENT_TYPE" => "application/json"
    assert_equal 201, last_response.status
    refute_includes Product.find_by(sku: "TEST-002").description, "<script>"
  end

  def test_import_feed_updates_quantities
    Product.create!(sku: "FEED-1", name: "Feed Item", quantity: 0)
    post "/import-feed",
         %(<feed><item sku="FEED-1" qty="42"/></feed>),
         "CONTENT_TYPE" => "application/xml"
    assert_equal 200, last_response.status
    assert_equal 42, Product.find_by(sku: "FEED-1").quantity
  end
end
