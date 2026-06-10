# frozen_string_literal: true

# Inventory Management API (Ruby edition).
#
# A small demo service used to test automated dependency-remediation agents.
# It deliberately exercises APIs from several pinned (outdated) gems so that
# an upgrade agent has real call sites to validate against.

require "sinatra/base"
require "active_record"
require "nokogiri"
require "rest-client"
require "loofah"
require "addressable/uri"
require "json"

ActiveRecord::Base.establish_connection(
  adapter: "sqlite3",
  database: ENV.fetch("DB_PATH", "inventory.db")
)

ActiveRecord::Schema.define do
  unless ActiveRecord::Base.connection.table_exists?(:products)
    create_table :products do |t|
      t.string  :sku,      null: false
      t.string  :name,     null: false
      t.text    :description
      t.integer :quantity, default: 0
      t.timestamps
    end
  end
end

class Product < ActiveRecord::Base
  validates :sku, :name, presence: true
end

class InventoryAPI < Sinatra::Base
  set :show_exceptions, false

  get "/health" do
    json_response(status: "ok")
  end

  get "/products" do
    products = Product.order(:sku).map do |p|
      { sku: p.sku, name: p.name, quantity: p.quantity }
    end
    json_response(products)
  end

  post "/products" do
    payload = JSON.parse(request.body.read)
    # Sanitize supplier-provided HTML descriptions before storing.
    description = Loofah.fragment(payload["description"].to_s).scrub!(:prune).to_s
    product = Product.create!(
      sku: payload.fetch("sku"),
      name: payload.fetch("name"),
      description: description,
      quantity: payload.fetch("quantity", 0)
    )
    status 201
    json_response(id: product.id)
  end

  # Parse a supplier's XML stock feed: <feed><item sku="A" qty="3"/></feed>
  post "/import-feed" do
    doc = Nokogiri::XML(request.body.read) { |cfg| cfg.nonet.noent }
    updated = 0
    doc.xpath("//item").each do |node|
      product = Product.find_by(sku: node["sku"])
      next unless product

      product.update!(quantity: node["qty"].to_i)
      updated += 1
    end
    json_response(updated: updated)
  end

  # Pull stock levels from an external supplier API.
  post "/sync-supplier" do
    payload = JSON.parse(request.body.read)
    uri = Addressable::URI.parse(payload.fetch("url"))
    halt 400, json_response(error: "http(s) only") unless %w[http https].include?(uri.scheme)

    resp = RestClient.get(uri.to_s, accept: :json)
    json_response(status_code: resp.code, bytes: resp.body.bytesize)
  end

  helpers do
    def json_response(obj)
      content_type :json
      JSON.generate(obj)
    end
  end
end
