package com.example.gamerecapplication.model

import java.io.Serializable

data class Price(
    var currency:String,
    var initial : Int,
    var final : Int,
    var discount_percent : Int,
    var initial_formatted : String,
    var final_formatted : String
): Serializable