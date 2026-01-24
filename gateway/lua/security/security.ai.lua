local json = require("cjson")
local waf = require("waf")

local body_lenght = tonumber(ngx.var.http_content_length) or 0
ngx.req.read_body()
local body = ngx.req.get_body_data()

local success, data = waf.validate(body, body_lenght)

if not success then 
    ngx.header["Content-Type"] = "application/json"
    ngx.say(json.encode({ error = data}))
    -- Status already set in waf.validate
    return ngx.exit(ngx.status)
end