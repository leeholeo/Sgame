package com.example.gamerecapplication.model

import com.google.gson.annotations.SerializedName
import java.io.Serializable
import kotlin.collections.ArrayList

data class SurveyResponse(
    @SerializedName("results")
    var results : ArrayList<SurveyResult>,
) : Serializable

data class SurveyResult(
    @SerializedName("question")
    var surveys : ArrayList<Survey>
): Serializable

data class Survey(
    var question : String,
    var answer : Answer,
): Serializable

data class Answer(
    var ans1 : String,
    var ans2 : String
): Serializable