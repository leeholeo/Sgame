package com.example.gamerecapplication.util

import com.example.gamerecapplication.model.FavoriteGame

object FavoriteGameSupporter {
    fun isFavorite(steam_appid : Int, favorite_list : ArrayList<FavoriteGame>) : Boolean{
        for(i in 0 until favorite_list.size){
            if(favorite_list[i].steam_appid.equals(steam_appid)){
                return true
            }
        }
        return false
    }
}