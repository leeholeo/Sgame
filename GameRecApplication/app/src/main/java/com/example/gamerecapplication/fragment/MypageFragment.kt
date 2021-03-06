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

    // ???????????? ????????? ?????? ??????
    var auth : FirebaseAuth?= null
    var googleSignInClient : GoogleSignInClient?= null

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // ?????? ??????????????? ??????????????? ????????? ??????
        mBinding = DataBindingUtil.inflate(inflater, R.layout.fragment_mypage, container, false)
        activity?.let {
            mBinding.lifecycleOwner = this
            mBinding.viewModel = model
        }

        mBinding.steamLink.setOnClickListener {showdialog()}
        Log.d("MyPage Fragment", "MyPage Fragment ?????????")
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
            Log.d("??????????????? ???????????? ???????????? ??????", "${model.favoriteGame.value?.size}")
            setFavViewPager()
        })

        model.recommendedGame.observe(viewLifecycleOwner, Observer { gamesList ->
            Log.d("???????????? ???????????? ???????????? ??????", "${model.recommendedGame.value?.size}")
            setRecViewPager()
        })
    }

    fun setRecViewPager(){
        // ??????, ????????? ?????? ??????
        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
        var screenWidth = resources.displayMetrics.widthPixels // ??????????????? ?????? ????????? ?????????
        var offsetPx = screenWidth - pageMarginPx - pagerWidth

        // Adapter Click Event
        recViewPagerAdapter = model.recommendedGame.value?.let { FavoriteViewPagerAdapter(it) }!!
        recViewPagerAdapter.notifyDataSetChanged()
        recViewPagerAdapter.setOnItemClickListener(object : FavoriteViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(context, GameActivity::class.java).apply {
                    // intent ?????? ???????????? ????????? url ????????????
                    putExtra("game",game)
                    putExtra("backFragment",R.id.third)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // ???????????? ( SDK ????????? ????????? ??????????????? ???????????? ?????????.)
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
        // viewPager ??????
        mBinding.recViewPager.adapter = recViewPagerAdapter
        mBinding.recViewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
        mBinding.recViewPager.offscreenPageLimit = 2 // ??? ?????? ???????????? ?????? ?????? ???????????????
        mBinding.recViewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
    }

    fun setFavViewPager(){
        // ??????, ????????? ?????? ??????
        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
        var screenWidth = resources.displayMetrics.widthPixels // ??????????????? ?????? ????????? ?????????
        var offsetPx = screenWidth - pageMarginPx - pagerWidth

        // Adapter Click Event
        favViewPagerAdapter = model.favoriteGame.value?.let { FavoriteViewPagerAdapter(it) }!!
        favViewPagerAdapter.notifyDataSetChanged()
        favViewPagerAdapter.setOnItemClickListener(object : FavoriteViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(context, GameActivity::class.java).apply {
                    // intent ?????? ???????????? ????????? url ????????????
                    putExtra("game",game)
                    putExtra("backFragment",R.id.third)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // ???????????? ( SDK ????????? ????????? ??????????????? ???????????? ?????????.)
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
        // viewPager ??????
        mBinding.favViewPager.adapter = favViewPagerAdapter
        mBinding.favViewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
        mBinding.favViewPager.offscreenPageLimit = 2 // ??? ?????? ???????????? ?????? ?????? ???????????????
        mBinding.favViewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
    }

//    //??????
//    private fun steamObservers() {
//        model.Id_games.observe(viewLifecycleOwner, Observer { gamesList ->
//            Log.d("??????????????? ???????????? ??????", "${model.Id_games.value?.size}")
//            steaminitView()
//        })
//    }

//    fun steaminitView(){
//        // ??????, ????????? ?????? ??????
//        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
//        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
//        var screenWidth = resources.displayMetrics.widthPixels // ??????????????? ?????? ????????? ?????????
//        var offsetPx = screenWidth - pageMarginPx - pagerWidth
//
//        // Adapter Click Event
//        steamViewPagerAdapter = model.Id_games.value?.let { SteamViewPagerAdapter(it as ArrayList<Game>) }!!
//        steamViewPagerAdapter.setOnItemClickListener(object : SteamViewPagerAdapter.OnItemClickListener{
//            override fun onItemClick(v: View, game: Game, pos: Int) {
//                Intent(context, GameActivity::class.java).apply {
//                    // intent ?????? ???????????? ????????? url ????????????
//                    putExtra("game",game)
//                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
//                }.run {
//                    // ???????????? ( SDK ????????? ????????? ??????????????? ???????????? ?????????.)
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
//        // viewPager ??????
//        mBinding.steamViewPager.adapter = steamViewPagerAdapter
//        mBinding.steamViewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
//        mBinding.steamViewPager.offscreenPageLimit = 2 // ??? ?????? ???????????? ?????? ?????? ???????????????
//        mBinding.steamViewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
//    }
    var m_Text = ""
    //?????? ?????? ?????? ???????????????
    fun showdialog(){
        val builder: AlertDialog.Builder = android.app.AlertDialog.Builder(this.context)
        builder.setTitle("Steam ???????????? ????????? ?????????\n(Steam -> ?????? ?????? -> ?????????)")

        // Set up the input
        val input = EditText(this.context)
        // Specify the type of input expected; this, for example, sets the input as a password, and will mask the text
        input.setHint("Steam ???????????? ????????? ?????????")
        input.inputType = InputType.TYPE_CLASS_TEXT
        builder.setView(input)

        // Set up the buttons
        builder.setPositiveButton("??????", DialogInterface.OnClickListener { dialog, which ->
            // Here you get get input text from the Edittext
            m_Text = input.text.toString()
            Log.d("m_Text", m_Text)

            pref = requireActivity().getPreferences(0)
            editor = pref.edit()
            editor.putString("InputData", m_Text)
            editor.apply()
        })
        builder.setNegativeButton("??????", DialogInterface.OnClickListener { dialog, which -> dialog.cancel() })

        builder.show()
    }

    fun logout(){
        // ?????? ??????????????? ?????? ????????? ?????? ????????????
        var gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(R.string.default_web_client_id))
            .requestEmail()
            .build()
        googleSignInClient = this.context?.let { GoogleSignIn.getClient(it, gso) }

        // firebaseauth??? ???????????? ?????? ???????????? get
        auth = FirebaseAuth.getInstance()

        // ?????? ???????????? ?????? ?????? ??? ?????????
        mBinding.btnLogout.setOnClickListener {
            FirebaseAuth.getInstance().signOut()
            googleSignInClient?.signOut()

            var logoutIntent = Intent(this.context, LoginActivity::class.java)
            logoutIntent.flags = Intent.FLAG_ACTIVITY_CLEAR_TASK or Intent.FLAG_ACTIVITY_NEW_TASK
            startActivity(logoutIntent)
        }
    }
}