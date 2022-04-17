package com.example.gamerecapplication.model

import java.io.Serializable

data class Screenshot(
    var id : Int,
    var path_thumbnail : String,
    var path_full : String
): Serializable
