local json = require("cjson")
local redis = require("resty.redis")
local red = redis:new()

red:set_timeout(1000)

local r_ok, r_err = red:connect("redis", 6379)

if not r_ok then
    ngx.log(ngx.ERR, "failed to connect to Redis: ", r_err)
    return
end

local latency = ngx.now() - ngx.req.start_time()

local body = ngx.ctx.response_body

if body then
    local ok, data = pcall(json.decode, body)
    if ok and data then
        local log = {
            timestamp = ngx.now(),
            method = ngx.req.get_method(),
            uri = ngx.var.request_uri,
            status = ngx.status,
            latency = string.format("%.3f", latency),
            client_ip = ngx.var.remote_addr,
            response_size = tonumber(ngx.var.bytes_sent) or 0,
            response_body = data,
            args = ngx.req.get_uri_args(),
        }

        local log_json = json.encode(log)
        red:rpush("api_logs", log_json)
        red:ltrim("api_logs", -1000, -1)
        red:expire("api_logs", 86400)
    end
end

red:set_keepalive(10000, 100)

ngx.ctx.buffered = nil
ngx.ctx.response_body = nil
collectgarbage("step")