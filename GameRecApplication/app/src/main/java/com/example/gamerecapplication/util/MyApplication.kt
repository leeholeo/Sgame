package com.example.gamerecapplication.util

import android.app.Application
import android.content.Context

// MyApplication.applicationContext()
class MyApplication : Application() {
    lateinit var context: Context

    init{
        instance = this
    }

    companion object {
        private var instance: MyApplication? = null
        fun applicationContext() : Context {
            return instance!!.applicationContext
        }
    }
}