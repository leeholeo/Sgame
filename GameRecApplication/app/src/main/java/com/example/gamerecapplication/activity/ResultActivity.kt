package com.example.gamerecapplication.activity

import android.app.ActivityOptions
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.databinding.DataBindingUtil
import com.example.gamerecapplication.R
import com.example.gamerecapplication.adapter.MainViewPagerAdapter
import com.example.gamerecapplication.adapter.ResultListAdapter
import com.example.gamerecapplication.databinding.ActivityResultBinding
import com.example.gamerecapplication.model.Game
import com.example.gamerecapplication.model.RecommendGames
import com.example.gamerecapplication.viewmodel.ResultViewModel
import com.google.firebase.auth.FirebaseUser

// Result Activity
// 설문 결과가 나올 창 - 설문 끝나면 게임 리스트를 보여줄거임
class ResultActivity : AppCompatActivity(){
    // view Binding
    private lateinit var rBinding: ActivityResultBinding
    private val model: ResultViewModel by viewModels()
    private var recList = ArrayList<Game>() //추천 리스트

    override fun onCreate(savedInstanceState: Bundle?) {
        // 모든 액티비티에 공통적으로 필요한 코드
        super.onCreate(savedInstanceState)
        rBinding = DataBindingUtil.setContentView(this, R.layout.activity_result)
        rBinding.lifecycleOwner = this
        rBinding.viewModel = model

        val recommendGames = intent.getSerializableExtra("gameList") as RecommendGames
        recList = recommendGames.list as ArrayList<Game>

        val resultListAdapter = ResultListAdapter(this, recList)
        resultListAdapter.setOnItemClickListener(object : ResultListAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(this@ResultActivity, GameActivity::class.java).apply {
                    putExtra("game",game)
                    putExtra("backFragment",-1)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // 화면전환 ( SDK 버전이 낮으면 화면전환을 지원하지 않는다. )
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                        var options : ActivityOptions = ActivityOptions.makeSceneTransitionAnimation(this@ResultActivity,
                            v.findViewById(R.id.gameBackground),"imageTransition")
                        startActivity(this, options.toBundle())
                    }else{
                        startActivity(this)
                    }
                }
            }
        })
        rBinding.listView.adapter = resultListAdapter

        // 메인으로 가기
        rBinding.btnGohome.setOnClickListener{
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }
    }

    override fun onBackPressed() {
        super.onBackPressed()
        startActivity(Intent(this, MainActivity::class.java))
        finish()
    }
}