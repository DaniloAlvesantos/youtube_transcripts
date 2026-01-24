local cjson = require("cjson")

ngx.header["Content-Type"] = "application/json"

local response = {
    message = "Lua script executed successfully",
    status = "success"
}

ngx.say(cjson.encode(response))
