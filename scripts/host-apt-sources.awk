# Rewrite recognized Ubuntu archive URIs while preserving source options and suites.
# Called before Python or additional APT tools have been installed.
# mode=uris lists enabled, recognized archive roots for download measurements.

function ubuntu_uri(uri, host, path) {
    if (uri !~ /^https?:\/\//) return 0
    host = uri
    sub(/^https?:\/\//, "", host)
    path = host
    sub(/^[^/]+/, "", path)
    sub(/\/.*/, "", host)
    if (path !~ /^\/ubuntu\/?$/) return 0
    return host ~ /(^|\.)archive\.ubuntu\.com$/ || host == "security.ubuntu.com" || \
        host == "mirrors.tuna.tsinghua.edu.cn" || host == "mirrors.aliyun.com" || \
        host == "mirrors.cloud.aliyuncs.com" || host == "mirrors.ustc.edu.cn" || \
        host == "mirrors.huaweicloud.com" || host == "repo.huaweicloud.com" || \
        host == "mirrors.cloud.tencent.com" || host == "mirrors.tencent.com" || \
        host == "mirrors.nju.edu.cn" || host == "mirrors.bfsu.edu.cn"
}

function rewrite(line, secure, rest, uri, result, target) {
    target = (choice == "tuna") ? "https://mirrors.tuna.tsinghua.edu.cn/ubuntu/" : \
        (secure ? "http://security.ubuntu.com/ubuntu/" : "http://archive.ubuntu.com/ubuntu/")
    rest = line
    result = ""
    while (match(rest, /https?:\/\/[^ \t\r]+/)) {
        result = result substr(rest, 1, RSTART - 1)
        uri = substr(rest, RSTART, RLENGTH)
        rest = substr(rest, RSTART + RLENGTH)
        if (ubuntu_uri(uri)) {
            recognized++
            if (mode == "uris") {
                sub(/\/$/, "", uri)
                print uri
            }
            if (uri != target) changed++
            uri = target
        }
        result = result uri
    }
    return result rest
}

function flush(    i, field, suites, disabled, count, parts, secure, ordinary, line) {
    if (!size) return
    field = ""
    suites = ""
    disabled = 0
    for (i = 1; i <= size; i++) {
        line = lines[i]
        if (line ~ /^[ \t]*#/) continue
        if (line ~ /^[^ \t#][^:]*:/) {
            field = tolower(line)
            sub(/:.*/, "", field)
        } else if (line !~ /^[ \t]/) {
            field = ""
        }
        if (tolower(line) ~ /^enabled:[ \t]*no[ \t\r]*$/) disabled = 1
        if (field == "suites") {
            sub(/^[Ss][Uu][Ii][Tt][Ee][Ss]:[ \t]*/, "", line)
            suites = suites " " line
        }
    }
    count = split(suites, parts, /[ \t\r]+/)
    secure = 0
    ordinary = 0
    for (i = 1; i <= count; i++) {
        if (parts[i] ~ /-security$/) secure = 1
        else if (parts[i] != "") ordinary = 1
    }
    # Mixed release/security stanzas can use the official archive for all suites.
    field = ""
    for (i = 1; i <= size; i++) {
        line = lines[i]
        if (line ~ /^[ \t]*#/) {
            if (mode != "uris") print line
            delete lines[i]
            continue
        }
        if (line ~ /^[^ \t#][^:]*:/) {
            field = tolower(line)
            sub(/:.*/, "", field)
        } else if (line !~ /^[ \t]/) {
            field = ""
        }
        if (!disabled && field == "uris") line = rewrite(line, secure && !ordinary)
        if (mode != "uris") print line
        delete lines[i]
    }
    size = 0
}

{
    if (format == "list") {
        line = $0
        if (line ~ /^[ \t]*deb(-src)?[ \t]+/) {
            # Leave comments, disabled sources, and third-party URLs untouched.
            comment = ""
            if (match(line, /[ \t]+#/)) {
                comment = substr(line, RSTART)
                line = substr(line, 1, RSTART - 1)
            }
            line = rewrite(line, line ~ /[ \t][^ \t]+-security[ \t]/) comment
        }
        if (mode != "uris") print line
    } else if ($0 ~ /^[ \t\r]*$/) {
        flush()
        if (mode != "uris") print
    } else {
        lines[++size] = $0
    }
}

END {
    if (format != "list") flush()
    if (mode == "uris") exit 0
    # Distinguish an already-selected source from an unrecognized configuration.
    if (!recognized) exit 4
    if (!changed) exit 3
}
