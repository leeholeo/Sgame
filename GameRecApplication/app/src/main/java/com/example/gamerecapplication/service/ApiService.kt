package com.example.gamerecapplication.service

import com.example.gamerecapplication.model.*
import retrofit2.Response
import retrofit2.http.*

interface ApiService {
    @POST("api/app")
    suspend fun createApp(
        @Body appId : App,
    )

    @POST("api/surveyResult")
    suspend fun createSurveyResult(
        @Body surveyAnswerResult: SurveyAnswerResult,
    )

    @PUT("api/surveyResult/{appId}")
    suspend fun updateSurveyResult(
        @Body surveyAnswerResult: SurveyAnswerResult,
        @Path("appId") appId: String
    )

    @GET("api/newGame")
    suspend fun getNewGame(
        @Query("limit") limit:Int,
        @Query("offset") offset:Int
    ):Response<GameResponse>

    @GET("api/surveyQuestion")
    suspend fun getSurvey(
        @Query("limit") limit:Int,
        @Query("offset") offset:Int
    ):Response<SurveyResponse>

    @GET("api/favorite/{appId}")
    suspend fun getFavorite(
        @Path("appId")appId : String,
    ):Response<Favorite>

    @PUT("api/favorite/{appId}")
    suspend fun updateFavorite(
        @Body data : Favorite,
        @Path("appId")appId : String,
    )

    @POST("api/favorite")
    suspend fun createFavorite(
        @Body data : Favorite
    )

    @GET("api/favorite/{appId}")
    suspend fun getApp(
        @Path("appId") appId: String
    ):Response<App>

    @GET("api/find/game/ACT/{index}")
    suspend fun getAct(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/ADV/{index}")
    suspend fun getAdv(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/CAS/{index}")
    suspend fun getCas(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/FRE/{index}")
    suspend fun getFre(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/IND/{index}")
    suspend fun getInd(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/MUL/{index}")
    suspend fun getMul(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/RAC/{index}")
    suspend fun getRac(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/RPG/{index}")
    suspend fun getRpg(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/SIG/{index}")
    suspend fun getSig(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/SPO/{index}")
    suspend fun getSpo(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

    @GET("api/find/game/STR/{index}")
    suspend fun getStr(
        @Path("index") index : Int
    ):Response<ArrayList<Game>>

//    @GET("api/find/game/{userId}")
//    suspend fun getId(
//        @Path("userId") userId : String
//    ):Response<List<Game>>

    @GET("api/survey/{user_id}")
    suspend fun getSurveyResult(
        @Path("user_id") appId : String,
    ):Response<List<Game>>

    @GET("api/popularGame")
    suspend fun getPopularGame(
        @Query("limit") limit : Int,
        @Query("offset") offset : Int
    ):Response<GameResponse>

    @GET("api/topCurrentPlayerGame")
    suspend fun getTopCurrentGame(
        @Query("limit") limit : Int,
        @Query("offset") offset : Int
    ):Response<GameResponse>

    @GET("api/topTodayPlayerGame")
    suspend fun getTodayGame(
        @Query("limit") limit : Int,
        @Query("offset") offset : Int
    ):Response<GameResponse>

    @GET("api/search/game/{gameName}")
    suspend fun searchGame(
        @Path("gameName") gameName : String
    ):Response<List<Game>>

    @GET("api/recommendationSurvey/game/{appid}")
    suspend fun getRecGame(
        @Path("appid") appId: String,
    ):Response<List<Game>>

    @GET("api/favorite/game/{appId}")
    suspend fun getFavoriteGame(
        @Path("appId")appId : String,
    ):Response<List<Game>>
}