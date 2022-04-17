package com.example.gamerecapplication.activity

import android.content.Context
import android.content.Intent
import android.graphics.Typeface
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.util.TypedValue
import android.view.Gravity
import android.view.LayoutInflater
import android.view.View
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.databinding.DataBindingUtil
import androidx.lifecycle.Observer
import androidx.viewpager2.widget.ViewPager2
import com.bumptech.glide.Glide
import com.example.gamerecapplication.R
import com.example.gamerecapplication.adapter.ScreenShotViewPagerAdapter
import com.example.gamerecapplication.databinding.ActivityGameBinding
import com.example.gamerecapplication.model.Favorite
import com.example.gamerecapplication.model.FavoriteGame
import com.example.gamerecapplication.model.Game
import com.example.gamerecapplication.service.GamesService
import com.example.gamerecapplication.util.FavoriteGameSupporter
import com.example.gamerecapplication.viewmodel.GameViewModel
import com.example.gamerecapplication.viewmodel.MainViewModel
import com.google.firebase.auth.FirebaseAuth
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.Dispatcher

class GameActivity : AppCompatActivity() {
    // view Binding
    private lateinit var gBinding: ActivityGameBinding
    private lateinit var game : Game
    private val model: GameViewModel by viewModels()
    private lateinit var favoriteList : ArrayList<FavoriteGame>

    override fun onCreate(savedInstanceState: Bundle?) {
        // 모든 액티비티에 공통적으로 필요한 코드
        super.onCreate(savedInstanceState)
        gBinding = DataBindingUtil.setContentView(this, R.layout.activity_game)
        gBinding.lifecycleOwner = this
        gBinding.viewModel = model

        game = intent.getSerializableExtra("game") as Game
        model.game.value = game

        // 액티비티 실행시 view
        setInitView()
        setFavorite()
        setScreenShotViewPager()

        //더보기 실행
        gBinding.viewMore.visibility = View.INVISIBLE
        setViewMore(gBinding.detailView, gBinding.viewMore)

        // 뒤로가기
        gBinding.btnBack.setOnClickListener{
            val next = intent.getIntExtra("backFragment",R.id.first)
            if(next == -1){
                finish()
            }else{
                val intent = Intent(this, MainActivity::class.java)
                intent.putExtra("backFragment",next)
                startActivity(intent)
            }
        }
    }

    // 현재 게임을 즐겨찾기 중인지 확인및 UI 변경
    fun setFavorite(){
        CoroutineScope(Dispatchers.Main).launch {
            val userId = FirebaseAuth.getInstance().currentUser?.uid
            val response = userId?.let { GamesService.getGamesService().getFavorite(it) }
            favoriteList = response?.body()?.gameList?:ArrayList()
            val isfav = favoriteList?.let { FavoriteGameSupporter.isFavorite(game.steam_appid, it) } ?: false

            // 현재게임이 즐겨찾기중인지 저장
            model.favorite.value = isfav
        }

        gBinding.favoriteImage.setOnClickListener {
            if(model.favorite.value == true){
                // 즐겨찾기 취소
                model.favorite.value = false
                CoroutineScope(Dispatchers.Main).launch {
                    val favgame = FavoriteGame(game.steam_appid)
                    val uid = FirebaseAuth.getInstance().uid
                    favoriteList.remove(favgame)
                    val fav = uid?.let { it1 -> Favorite(it1, favoriteList) }
                    uid?.let { it1 ->
                        fav?.let { it2 ->
                            GamesService.getGamesService().updateFavorite(
                                it2, it1
                            )
                        }
                    }
                }
            }else{
                // 즐겨찾기
                model.favorite.value = true
                CoroutineScope(Dispatchers.Main).launch {
                    val favgame = FavoriteGame(game.steam_appid)
                    val uid = FirebaseAuth.getInstance().uid
                    favoriteList.add(favgame)
                    val fav = uid?.let { it1 -> Favorite(it1,favoriteList) }
                    uid?.let { it1 -> fav?.let { it2 ->
                        GamesService.getGamesService().updateFavorite(
                            it2, it1)
                    } }
                }
            }
        }
    }

    fun setInitView(){
        // header image
        Glide.with(this)
            .load(game.header_image)
            .placeholder(R.drawable.game1)
            .override(resources.displayMetrics.widthPixels)
            .into(gBinding.imageView)

        // favorite
        model.favorite.observe(this, Observer {
            if(it){
                gBinding.favoriteImage.setImageResource(R.drawable.favorite_icon)
                Log.d("Favorite", "좋아하는게임")


            }else{
                gBinding.favoriteImage.setImageResource(R.drawable.empty_icon)
                Log.d("Favorite", "안좋아하는게임")
            }
        })

        // homepage
        model.toast.observe(this, Observer {
            if(it){
                model.toast.value = false
                Toast.makeText(this@GameActivity,"웹 페이지가 존재하지 않습니다.", Toast.LENGTH_SHORT).show()
            }
        })

        // publisher
        model.publisher.value = game?.publishers?.get(0)

        // category
        val params : LinearLayout.LayoutParams = LinearLayout.LayoutParams(dpToPx(this,60f), dpToPx(this,30f))
        params.rightMargin = 20
        for(i in 0 until game.genres.size){
            if(i >= 5) break
            val tv = TextView(this)
            tv.text = game.genres[i].description
            tv.gravity = Gravity.CENTER
            tv.textSize = 12f
            tv.setTypeface(tv.typeface,Typeface.BOLD)
            tv.background = resources.getDrawable(R.drawable.category_round)
            tv.layoutParams = params
            gBinding.categoryLayout.addView(tv)
        }
    }

    fun dpToPx(context : Context, dp:Float) : Int{
        return TypedValue.applyDimension(
            TypedValue.COMPLEX_UNIT_DIP,
            dp,
            context.resources.displayMetrics
        ).toInt()
    }

    // 게임 스크린샷 viewPager
    fun setScreenShotViewPager(){
        // 여백, 너비에 대한 정의
        val pageMarginPx = resources.getDimensionPixelOffset(R.dimen.screenViewPageMargin)
        val pagerWidth = resources.getDimensionPixelOffset(R.dimen.screenViewPageWidth)
        val screenWidth = resources.displayMetrics.widthPixels // 스마트폰의 너비 길이를 가져옴
        val offsetPx = screenWidth - pageMarginPx - pagerWidth

        // Adapter Click Event
        val viewPagerAdapter = ScreenShotViewPagerAdapter(game.screenshots)
        viewPagerAdapter.setOnItemClickListener(object : ScreenShotViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, data: String, pos: Int) {
                v.setOnClickListener {
                    val dialogView  = LayoutInflater.from(this@GameActivity).inflate(R.layout.screenshot_dialog,null)
                    val mBuilder = AlertDialog
                        .Builder(this@GameActivity)
                        .setView(dialogView)
                    Glide.with(this@GameActivity)
                        .load(data)
                        .override(resources.displayMetrics.widthPixels)
                        .into(dialogView.findViewById(R.id.imageView))
                    mBuilder.show()
                }
            }
        })

        // viewPager 생성
        gBinding.viewPager.adapter = viewPagerAdapter
        gBinding.viewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
        gBinding.viewPager.offscreenPageLimit = 1 // 몇 개의 페이지를 미리 로드 해둘것인지
        gBinding.viewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
    }

    // 더보기 표시
    private fun setViewMore(detailView: TextView, viewMoreTextView: TextView) {
        // getEllipsisCount()을 통한 더보기 표시 및 구현
        detailView.post {
            val lineCount = detailView.layout.lineCount
            if (lineCount > 1) {
                if (detailView.layout.getEllipsisCount(lineCount - 1) > 0) {
                    // 더보기 표시
                    viewMoreTextView.visibility = View.VISIBLE

                    // 더보기 클릭 이벤트
                    viewMoreTextView.setOnClickListener {
                        detailView.maxLines = Int.MAX_VALUE
                        viewMoreTextView.visibility = View.GONE
                    }
                }
            }
        }
    }
}