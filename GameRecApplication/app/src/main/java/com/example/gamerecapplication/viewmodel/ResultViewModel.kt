package com.example.gamerecapplication.viewmodel

import android.content.Intent
import android.net.Uri
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.gamerecapplication.model.Game
import com.example.gamerecapplication.model.SurveyAnswerResult
import com.example.gamerecapplication.util.MyApplication

class ResultViewModel(): ViewModel() {
    //LiveData
    //값이 변경되는 경우 MutableLiveData로 선언한다.
    var game = MutableLiveData<Game>()
    var publisher = MutableLiveData<String>()
}