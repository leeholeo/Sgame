package com.example.gamerecapplication.model

data class Favorite(
    val appId : String,
    val gameList : ArrayList<FavoriteGame>
)

data class FavoriteGame(
    val steam_appid : Int
)