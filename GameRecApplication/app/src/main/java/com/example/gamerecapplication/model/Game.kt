package com.example.gamerecapplication.model

import com.google.gson.annotations.SerializedName
import java.io.Serializable
import kotlin.collections.ArrayList

data class GameResponse(
    @SerializedName("results")
    val results : ArrayList<Game>,
) : Serializable

data class Game (
    var _id : String,
    var name : String,
    var steam_appid : Int,
    var requiredAge : Int,
    var detailed_description: String,
    var about_the_game : String,
    var short_description: String,
    var header_image: String,
    var website : String?,
    //var pc_requirements : Data,
    var legal_notice : String,
    //var developers : ArrayList<String?>,
    var publishers : ArrayList<String>,
    var price_overview: Price,
    //var metacritic: Objects,
    //var categories: ArrayList<Category>,
    var genres: ArrayList<Category>,
    var screenshots : ArrayList<Screenshot>,
    //var movies : ArrayList<Objects>,
    //var release_date : String,
    var background : String,
    var background_raw : String,
    var reviewRating : String
) : Serializable

data class RecommendGames(
    var list : List<Game>
):Serializable