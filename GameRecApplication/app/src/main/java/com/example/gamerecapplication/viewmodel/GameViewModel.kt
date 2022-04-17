package com.example.gamerecapplication.viewmodel

import android.content.Intent
import android.content.Intent.FLAG_ACTIVITY_NEW_TASK
import android.net.Uri
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.gamerecapplication.model.Game
import com.example.gamerecapplication.util.MyApplication

class GameViewModel: ViewModel() {
    //LiveData
    //값이 변경되는 경우 MutableLiveData로 선언한다.
    var game = MutableLiveData<Game>()
    var publisher = MutableLiveData<String>()
    var toast = MutableLiveData<Boolean>()
    var favorite = MutableLiveData<Boolean>()

    fun accessHomePage(){
        if(game.value?.website == null){
            toast.value = true
        }else{
            MyApplication.applicationContext().startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(game.value?.website)).addFlags(FLAG_ACTIVITY_NEW_TASK))
        }
    }
}