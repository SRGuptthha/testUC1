# frozen_string_literal: true

require "rack"
require "omniauth"
require_relative "app/api"

use Rack::Session::Cookie, secret: ENV.fetch("SESSION_SECRET", "dev-secret-change-me")

# Placeholder developer-mode auth strategy; swap for a real provider in prod.
use OmniAuth::Builder do
  provider :developer unless ENV["RACK_ENV"] == "production"
end

run InventoryAPI
