local chunk, is_eof = ngx.arg[1], ngx.arg[2]

-- Create a buffer in memory to store the body
if not ngx.ctx.buffered then
    ngx.ctx.buffered = {}
end

-- Append the current chunk to the buffer
if chunk ~= "" then
    table.insert(ngx.ctx.buffered, chunk)
end

if is_eof then
    -- Full body has been read; concatenate all chunks
    ngx.ctx.response_body = table.concat(ngx.ctx.buffered)
end