package dev.lscythe.app.kemana

interface Platform {
    val name: String
}

expect fun getPlatform(): Platform
