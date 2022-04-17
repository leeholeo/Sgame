package com.example.gamerecapplication.fragment

import android.app.ActivityOptions
import android.app.AlertDialog
import android.content.Context
import android.content.DialogInterface
import android.content.Intent
import android.content.SharedPreferences
import android.os.Build
import android.os.Bundle
import android.text.InputType
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import androidx.viewpager2.widget.ViewPager2
import com.example.gamerecapplication.R
import com.example.gamerecapplication.activity.GameActivity
import com.example.gamerecapplication.activity.LoginActivity
import com.example.gamerecapplication.adapter.FavoriteViewPagerAdapter
import com.example.gamerecapplication.adapter.SteamViewPagerAdapter
import com.example.gamerecapplication.adapter.ViewPagerAdapter
import com.example.gamerecapplication.databinding.FragmentMypageBinding
import com.example.gamerecapplication.model.Game
import com.example.gamerecapplication.viewmodel.MainViewModel
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.firebase.auth.FirebaseAuth

class MypageFragment : Fragment() {
    // view Binding
    private lateinit var mBinding: FragmentMypageBinding
    private lateinit var favViewPagerAdapter : FavoriteViewPagerAdapter
    private lateinit var recViewPagerAdapter : FavoriteViewPagerAdapter
    private val model: MainViewModel by viewModels()
    lateinit var pref : SharedPreferences
    lateinit var editor : SharedPreferences.Editor

//    private lateinit var steamViewPagerAdapter : SteamViewPagerAdapter

//    override fun onCreate(savedInstanceState: Bundle?) {
//        super.onCreate(savedInstanceState)
//    }

    // 로그아웃 구현을 위한 변수
    var auth : FirebaseAuth?= null
    var googleSignInClient : GoogleSignInClient?= null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // 모든 액티비티에 공통적으로 필요한 코드
        mBinding = DataBindingUtil.inflate(inflater, R.layout.fragment_mypage, container, false)
        activity?.let {
            mBinding.lifecycleOwner = this
            mBinding.viewModel = model
        }

        mBinding.steamLink.setOnClickListener {showdialog()}
        Log.d("MyPage Fragment", "MyPage Fragment 초기화")
        subscribeObservers()
        //steamObservers()
        logout()

        return mBinding.root
    }

    override fun onResume() {
        super.onResume()

        val ft = fragmentManager?.beginTransaction()
        ft?.detach(this)?.attach(this)?.commitAllowingStateLoss()
    }

    fun subscribeObservers() {
        model.favoriteGame.observe(viewLifecycleOwner, Observer { gamesList ->
            Log.d("즐겨찾기한 게임목록 불러오기 완료", "${model.favoriteGame.value?.size}")
            setFavViewPager()
        })

        model.recommendedGame.observe(viewLifecycleOwner, Observer { gamesList ->
            Log.d("추천받은 게임목록 불러오기 완료", "${model.recommendedGame.value?.size}")
            setRecViewPager()
        })
    }

    fun setRecViewPager(){
        // 여백, 너비에 대한 정의
        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
        var screenWidth = resources.displayMetrics.widthPixels // 스마트폰의 너비 길이를 가져옴
        var offsetPx = screenWidth - pageMarginPx - pagerWidth

        // Adapter Click Event
        recViewPagerAdapter = model.recommendedGame.value?.let { FavoriteViewPagerAdapter(it) }!!
        recViewPagerAdapter.notifyDataSetChanged()
        recViewPagerAdapter.setOnItemClickListener(object : FavoriteViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(context, GameActivity::class.java).apply {
                    // intent 안에 이름이랑 이미지 url 넣어주기
                    putExtra("game",game)
                    putExtra("backFragment",R.id.third)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // 화면전환 ( SDK 버전이 낮으면 화면전환을 지원하지 않는다.)
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                        var options : ActivityOptions = ActivityOptions.makeSceneTransitionAnimation(activity,
                            v.findViewById(R.id.gameImageView),"imageTransition")
                        startActivity(this, options.toBundle())
                    }else{
                        startActivity(this)
                    }
                }
            }
        })
        // viewPager 생성
        mBinding.recViewPager.adapter = recViewPagerAdapter
        mBinding.recViewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
        mBinding.recViewPager.offscreenPageLimit = 2 // 몇 개의 페이지를 미리 로드 해둘것인지
        mBinding.recViewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
    }

    fun setFavViewPager(){
        // 여백, 너비에 대한 정의
        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
        var screenWidth = resources.displayMetrics.widthPixels // 스마트폰의 너비 길이를 가져옴
        var offsetPx = screenWidth - pageMarginPx - pagerWidth

        // Adapter Click Event
        favViewPagerAdapter = model.favoriteGame.value?.let { FavoriteViewPagerAdapter(it) }!!
        favViewPagerAdapter.notifyDataSetChanged()
        favViewPagerAdapter.setOnItemClickListener(object : FavoriteViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(context, GameActivity::class.java).apply {
                    // intent 안에 이름이랑 이미지 url 넣어주기
                    putExtra("game",game)
                    putExtra("backFragment",R.id.third)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // 화면전환 ( SDK 버전이 낮으면 화면전환을 지원하지 않는다.)
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
                        var options : ActivityOptions = ActivityOptions.makeSceneTransitionAnimation(activity,
                            v.findViewById(R.id.gameImageView),"imageTransition")
                        startActivity(this, options.toBundle())
                    }else{
                        startActivity(this)
                    }
                }
            }
        })
        // viewPager 생성
        mBinding.favViewPager.adapter = favViewPagerAdapter
        mBinding.favViewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
        mBinding.favViewPager.offscreenPageLimit = 2 // 몇 개의 페이지를 미리 로드 해둘것인지
        mBinding.favViewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
    }

//    //스팀
//    private fun steamObservers() {
//        model.Id_games.observe(viewLifecycleOwner, Observer { gamesList ->
//            Log.d("라이브러리 불러오기 완료", "${model.Id_games.value?.size}")
//            steaminitView()
//        })
//    }

//    fun steaminitView(){
//        // 여백, 너비에 대한 정의
//        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
//        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
//        var screenWidth = resources.displayMetrics.widthPixels // 스마트폰의 너비 길이를 가져옴
//        var offsetPx = screenWidth - pageMarginPx - pagerWidth
//
//        // Adapter Click Event
//        steamViewPagerAdapter = model.Id_games.value?.let { SteamViewPagerAdapter(it as ArrayList<Game>) }!!
//        steamViewPagerAdapter.setOnItemClickListener(object : SteamViewPagerAdapter.OnItemClickListener{
//            override fun onItemClick(v: View, game: Game, pos: Int) {
//                Intent(context, GameActivity::class.java).apply {
//                    // intent 안에 이름이랑 이미지 url 넣어주기
//                    putExtra("game",game)
//                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
//                }.run {
//                    // 화면전환 ( SDK 버전이 낮으면 화면전환을 지원하지 않는다.)
//                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
//                        var options : ActivityOptions = ActivityOptions.makeSceneTransitionAnimation(activity,
//                            v.findViewById(R.id.gameImageView),"imageTransition")
//                        startActivity(this, options.toBundle())
//                    }else{
//                        startActivity(this)
//                    }
//                }
//            }
//        })
//        // viewPager 생성
//        mBinding.steamViewPager.adapter = steamViewPagerAdapter
//        mBinding.steamViewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
//        mBinding.steamViewPager.offscreenPageLimit = 2 // 몇 개의 페이지를 미리 로드 해둘것인지
//        mBinding.steamViewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
//    }
    var m_Text = ""
    //스팀 계정 연동 다이얼로그
    fun showdialog(){
        val builder: AlertDialog.Builder = android.app.AlertDialog.Builder(this.context)
        builder.setTitle("Steam 닉네임을 입력해 주세요\n(Steam -> 계정 정보 -> 닉네임)")

        // Set up the input
        val input = EditText(this.context)
        // Specify the type of input expected; this, for example, sets the input as a password, and will mask the text
        input.setHint("Steam 닉네임을 입력해 주세요")
        input.inputType = InputType.TYPE_CLASS_TEXT
        builder.setView(input)

        // Set up the buttons
        builder.setPositiveButton("연동", DialogInterface.OnClickListener { dialog, which ->
            // Here you get get input text from the Edittext
            m_Text = input.text.toString()
            Log.d("m_Text", m_Text)

            pref = requireActivity().getPreferences(0)
            editor = pref.edit()
            editor.putString("InputData", m_Text)
            editor.apply()
        })
        builder.setNegativeButton("취소", DialogInterface.OnClickListener { dialog, which -> dialog.cancel() })

        builder.show()
    }

    fun logout(){
        // 구글 로그아웃을 위해 로그인 세션 가져오기
        var gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(R.string.default_web_client_id))
            .requestEmail()
            .build()
        googleSignInClient = this.context?.let { GoogleSignIn.getClient(it, gso) }

        // firebaseauth를 사용하기 위한 인스턴스 get
        auth = FirebaseAuth.getInstance()

        // 구글 로그아웃 버튼 클릭 시 이벤트
        mBinding.btnLogout.setOnClickListener {
            FirebaseAuth.getInstance().signOut()
            googleSignInClient?.signOut()

            var logoutIntent = Intent(this.context, LoginActivity::class.java)
            logoutIntent.flags = Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK
            startActivity(logoutIntent)
        }
    }
}