local json = require("cjson")
local _M = {}

function _M.validate(body, body_lenght)
    -- Check if request body is present
    if not body or body_lenght == 0 then
        ngx.status = 400
        return false, "Request body is required"
    end

    -- Limit body size to 100KB
    if body_lenght > 1024 * 100 then
        ngx.status = 413
        return false, "Request body is too large"
    end

    -- Check if JSON decoding was successfully
    local ok, data = pcall(json.decode, body)
    if not ok or not data then
        ngx.status = 400
        return false, "Invalid request body"
    end

    return true, data
end

return _M