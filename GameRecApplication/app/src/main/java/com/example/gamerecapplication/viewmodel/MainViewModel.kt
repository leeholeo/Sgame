package com.example.gamerecapplication.viewmodel

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import com.example.gamerecapplication.model.*
import com.example.gamerecapplication.service.GamesService
import com.example.gamerecapplication.fragment.MypageFragment
import com.example.gamerecapplication.util.Event
import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.*

private lateinit var mypageFragment : MypageFragment

class MainViewModel(): ViewModel() {
    private val _showAnimation = MutableLiveData<Event<Boolean>>()
    val showAnimation: LiveData<Event<Boolean>> = _showAnimation

    //LiveData
    var currentSurvey = MutableLiveData<Int>()          // 현재 질문 번호
    var maxSurvey = MutableLiveData<Int>()              // 질문 개수
    var progressText = MutableLiveData<String>()        // 설문 번호 txt
    var numberText = MutableLiveData<String>()          // 설문 진행상황 txt
    var currentSurveyText = MutableLiveData<String>()   // 현재 질문

    var currentAnswer1 = MutableLiveData<String>()
    var currentAnswer2 = MutableLiveData<String>()

    var index = 0
    val findSize = 30

    // Coroutine
    var job : Job? = null
    val exceptionHandler = CoroutineExceptionHandler{
        coroutineContext, throwable ->
        onError("Exception: ${throwable.localizedMessage}")
    }
    val loadError = MutableLiveData<String?>()

    // Game Data
    val gamesService = GamesService.getGamesService()
    val favoriteGame = MutableLiveData<List<Game>>()
    val recommendedGame = MutableLiveData<List<Game>>()
    val recommendGame = MutableLiveData<RecommendGames>()

    val new_games = MutableLiveData<ArrayList<Game>>()
    val pop_games = MutableLiveData<ArrayList<Game>>()
    val cur_games = MutableLiveData<ArrayList<Game>>()
    val tod_games = MutableLiveData<ArrayList<Game>>()

    val act_games = MutableLiveData<ArrayList<Game>>()
    val adv_games = MutableLiveData<ArrayList<Game>>()
    val cas_games = MutableLiveData<ArrayList<Game>>()
    val fre_games = MutableLiveData<ArrayList<Game>>()
    val ind_games = MutableLiveData<ArrayList<Game>>()
    val mul_games = MutableLiveData<ArrayList<Game>>()
    val rac_games = MutableLiveData<ArrayList<Game>>()
    val rpg_games = MutableLiveData<ArrayList<Game>>()
    val sig_games = MutableLiveData<ArrayList<Game>>()
    val spo_games = MutableLiveData<ArrayList<Game>>()
    val str_games = MutableLiveData<ArrayList<Game>>()

    // Survey Data
    val surveys = MutableLiveData<ArrayList<Survey>>()
    var surveyResult = MutableLiveData<ArrayList<SurveyAnswer>>()
    var surveyEnd = MutableLiveData<Boolean>()
    var recommendEnd = MutableLiveData<Boolean>()

    // Steam Id
    //val Id_games = MutableLiveData<List<Game>>()

    // 초기화
    init {
        currentSurvey.value = 0
        maxSurvey.value = 10
        progressText.value = "${currentSurvey.value} / ${maxSurvey.value}"
        numberText.value = "Q${currentSurvey.value}"
        surveyResult.value = ArrayList()

        recommendGame.value = RecommendGames(listOf())
        refresh()
    }

    fun refresh(){
        fetchTopCurrentGame()
        fetchTodayGame()
        fetchPopularGame()
        fetchNewGames()
        fetchSurvey()
        fetchFavorite()
        fetchRecGame()

        findActGame()
        findAdvGame()
        findCasGame()
        findFreGame()
        findIndGame()
        findMulGame()
        findRacGame()
        findRpgGame()
        findSigGame()
        findSpoGame()
        findStrGame()
    }

    // DB에서 즐겨찾기한 게임목록을 가져온다.
    fun fetchRecGame(){
        Log.d("추천받았던 게임목록 불러오기 완료", "fetchFavorite")
        val uid = FirebaseAuth.getInstance().currentUser?.uid
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = uid?.let { gamesService.getRecGame(it) }
            withContext(Dispatchers.Main){
                if(response?.isSuccessful == true){
                    recommendedGame.value = response.body()
                }else {
                    onError("Error : ${response?.message()}")
                }
            }
        }
    }

    // DB에서 즐겨찾기한 게임목록을 가져온다.
    fun fetchFavorite(){
        val uid = FirebaseAuth.getInstance().currentUser?.uid
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = uid?.let { gamesService.getFavoriteGame(it) }
            withContext(Dispatchers.Main){
                if(response?.isSuccessful == true){
                    favoriteGame.value = response.body()
                }else {
                    onError("Error : ${response?.message()}")
                }
            }
        }
    }

    private fun fetchTopCurrentGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getTopCurrentGame(findSize,0)
            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    cur_games.value = response.body()?.results
                    loadError.value = null
                } else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun fetchTodayGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getTodayGame(findSize,0)
            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    tod_games.value = response.body()?.results
                    loadError.value = null
                } else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun fetchPopularGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getPopularGame(findSize,0)
            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    pop_games.value = response.body()?.results
                    loadError.value = null
                } else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findActGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getAct(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    act_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findAdvGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getAdv(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    adv_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findCasGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getCas(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    cas_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findFreGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getFre(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    fre_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findIndGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getInd(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    ind_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findMulGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getMul(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    mul_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findRacGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getRac(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    rac_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findRpgGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getRpg(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    rpg_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findSigGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getSig(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    sig_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findSpoGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getSpo(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    spo_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    private fun findStrGame(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getStr(findSize)
            withContext(Dispatchers.Main){
                if(response.isSuccessful){
                    str_games.value = response.body()
                }else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    // DB에서 인기게임 목록을 받아온다
    private fun fetchNewGames(){
        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
            val response = gamesService.getNewGame(40,0)
            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    new_games.value = response.body()?.results
                    loadError.value = null
                } else {
                    onError("Error : ${response.message()}")
                }
            }
        }
    }

    // DB에서 설문 목록을 받아온다
    private fun fetchSurvey(){
        job = CoroutineScope(Dispatchers.IO).launch {
            val response2 = gamesService.getSurvey(maxSurvey.value?:10,0)
            withContext(Dispatchers.Main){
                if (response2.isSuccessful) {
                    surveys.value = response2.body()?.results?.get(0)?.surveys
                    setSurvey()

                    loadError.value = null
                }else{
                    onError("Error : ${response2.message()}")
                }
            }
        }
    }



//    // DB에서 사용자 닉네임으로 검색한다
//    private fun fetchIdgames(){
//        Log.d("라이브러리 불러오기 완료", "fetchIdgames")
//        val id = mypageFragment.m_Text // text에서 id를 가져옴
//        job = CoroutineScope(Dispatchers.IO + exceptionHandler).launch {
//            val response = id?.let { gamesService.getId(it) }
//            withContext(Dispatchers.Main){
//                if(response?.isSuccessful == true){
//                    Log.d("라이브러리 불러오기 완료", "${response.body()?.size}")
//                    Id_games.value = response.body()
//                }else {
//                    onError("Error : ${response?.message()}")
//                }
//            }
//        }
//    }

    fun setSurvey(){
        // 화면에 나타날 값 변경
        progressText.postValue("${index + 1} / ${maxSurvey.value}")
        numberText.postValue("Q${index + 1}")

        currentSurveyText.postValue(surveys.value?.get(index)?.question)
        currentAnswer1.postValue(surveys.value?.get(index)?.answer?.ans1)
        currentAnswer2.postValue(surveys.value?.get(index)?.answer?.ans2)

        currentSurvey.postValue(++index)
    }

    // 설문을 진행할때마다 실행
    fun nextSurvey(){
        // 설문 종료
        if(index >= 10){
            CoroutineScope(Dispatchers.Main).launch {
                val user = FirebaseAuth.getInstance()
                val surveyAnswerResult = SurveyAnswerResult(user.uid?:"None",surveyResult.value?:ArrayList())

                user.uid?.let { gamesService.updateSurveyResult(surveyAnswerResult, it) }
                Log.d("Survet End" , "설문 조사 종료 ${user.uid} , ${surveyResult.value?.size}")
                surveyEnd.value = true
                val response = user.uid?.let { gamesService.getSurveyResult(it) }
                recommendGame.value?.list = response?.body()!!
                recommendEnd.value = true
                Log.d("추천 결과", "${response?.message()} , 추천 알고리즘 완료")
            }
            return
        }

        // 애니메이션 실행
        _showAnimation.value = Event(true)
        GlobalScope.launch(Dispatchers.Main) {
            delay(800)
            setSurvey()
        }
    }

    fun answer1(){
        if(index <= 10){
            val answer = SurveyAnswer(1)
            surveyResult.value?.add(answer)
            Log.d("??","${surveyResult.value?.size}")
        }
        nextSurvey()
    }

    fun answer2(){
        if(index <= 10){
            val answer = SurveyAnswer(-1)
            surveyResult.value?.add(answer)
        }
        nextSurvey()
    }

    private fun onError(message: String) {
        loadError.value = message
    }

    override fun onCleared() {
        super.onCleared()
        job?.cancel()
    }
}
