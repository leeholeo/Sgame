package com.example.gamerecapplication.fragment

import android.app.ActivityOptions
import android.content.Intent
import android.graphics.Typeface
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.LinearLayout
import android.widget.SearchView
import android.widget.TextView
import androidx.core.view.marginBottom
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.FragmentActivity
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import androidx.viewpager.widget.ViewPager
import androidx.viewpager2.adapter.FragmentStateAdapter
import androidx.viewpager2.widget.ViewPager2
import com.example.gamerecapplication.R
import com.example.gamerecapplication.activity.GameActivity
import com.example.gamerecapplication.activity.MainActivity
import com.example.gamerecapplication.adapter.ViewPagerAdapter
import com.example.gamerecapplication.databinding.FragmentHomeBinding
import com.example.gamerecapplication.model.Game
import com.example.gamerecapplication.adapter.MainViewPagerAdapter
import com.example.gamerecapplication.service.GamesService
import com.example.gamerecapplication.viewmodel.MainViewModel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.currentCoroutineContext
import kotlinx.coroutines.launch

class HomeFragment() : Fragment(){
    // view Binding
    private lateinit var hBinding: FragmentHomeBinding
    private val model: MainViewModel by viewModels()

    var currentPage = 0

    private var popularAdapter = ViewPagerAdapter()
    private var topCurrentAdapter = ViewPagerAdapter()
    private var todayAdapter = ViewPagerAdapter()

    private var actAdapter = ViewPagerAdapter()
    private var advAdapter = ViewPagerAdapter()
    private var casAdapter = ViewPagerAdapter()
    private var freAdapter = ViewPagerAdapter()
    private var indAdapter = ViewPagerAdapter()
    private var mulAdapter = ViewPagerAdapter()
    private var racAdapter = ViewPagerAdapter()
    private var rpgAdapter = ViewPagerAdapter()
    private var sigAdapter = ViewPagerAdapter()
    private var spoAdapter = ViewPagerAdapter()
    private var strAdapter = ViewPagerAdapter()

    private lateinit var mainViewPagerAdapter : MainViewPagerAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // ?????? ??????????????? ??????????????? ????????? ??????
        hBinding = DataBindingUtil.inflate(inflater,R.layout.fragment_home,container,false)
        activity?.let {
            hBinding.lifecycleOwner = this
            hBinding.viewModel = model
        }

        setMainViewPager()

        setViewPagerView("?????? ??????", popularAdapter)
        setViewPagerView("?????? ?????? ???????????? ?????? ?????? ??????", topCurrentAdapter)
        setViewPagerView("?????? ?????? ???????????? ?????? ?????? ??????", todayAdapter)

        setViewPagerView("?????? ??????", actAdapter)
        setViewPagerView("???????????? ??????", advAdapter)
        setViewPagerView("????????? ??????", casAdapter)
        setViewPagerView("?????? ??????", freAdapter)
        setViewPagerView("?????? ??????", indAdapter)
        setViewPagerView("?????? ???????????? ??????", mulAdapter)
        setViewPagerView("????????? ??????", racAdapter)
        setViewPagerView("RPG ??????", rpgAdapter)
        setViewPagerView("?????? ??????", sigAdapter)
        setViewPagerView("????????? ??????", spoAdapter)
        setViewPagerView("?????? ??????", strAdapter)

        subscribeObservers()

        hBinding.searchBar.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
            override fun onQueryTextSubmit(query: String?): Boolean {
                query?.let { searchGame(it) }
                return false
            }

            override fun onQueryTextChange(newText: String?): Boolean {
                return false
            }
        })

        //???????????? ????????? ?????????
        val thread=Thread(PagerRunnable())
        thread.start()
        return hBinding.root
    }

    fun searchGame(query : String){
        Log.d("searchGame", query)
        CoroutineScope(Dispatchers.Main).launch {
            val gamesService = GamesService.getGamesService()
            val response = gamesService.searchGame(query)
            Log.d("????????????", "${response.message()}, ${response.body()}")
        }
    }

    val handler = Handler(Looper.getMainLooper()){
        setPage()
        true
    }

    //????????? ????????????
    fun setPage(){
        if(currentPage == MainViewPagerAdapter.ITEM_COUNT)
            currentPage = 0
        hBinding.mainViewPager.setCurrentItem(currentPage, true)
        currentPage+=1
    }

    inner class PagerRunnable:Runnable{
        override fun run() {
            while(true){
                try {
                    Thread.sleep(5000)
                    handler.sendEmptyMessage(0)
                } catch (e : InterruptedException){
                    Log.d("interupt", "interupt??????")
                }
            }
        }
    }

    private fun subscribeObservers() {
        model.new_games.observe(viewLifecycleOwner, Observer { gamesList ->
            mainViewPagerAdapter.submitList(gamesList)
        })

        model.pop_games.observe(viewLifecycleOwner, Observer { gamesList ->
            popularAdapter.submitList(gamesList)
        })

        model.tod_games.observe(viewLifecycleOwner, Observer { gamesList ->
            todayAdapter.submitList(gamesList)
        })

        model.cur_games.observe(viewLifecycleOwner, Observer { gamesList ->
            topCurrentAdapter.submitList(gamesList)
        })

        model.act_games.observe(viewLifecycleOwner, Observer { gamesList ->
            actAdapter.submitList(gamesList)
        })

        model.adv_games.observe(viewLifecycleOwner, Observer { gamesList ->
            advAdapter.submitList(gamesList)
        })

        model.cas_games.observe(viewLifecycleOwner, Observer { gamesList ->
            casAdapter.submitList(gamesList)
        })

        model.fre_games.observe(viewLifecycleOwner, Observer { gamesList ->
            freAdapter.submitList(gamesList)
        })

        model.ind_games.observe(viewLifecycleOwner, Observer { gamesList ->
            indAdapter.submitList(gamesList)
        })

        model.mul_games.observe(viewLifecycleOwner, Observer { gamesList ->
            mulAdapter.submitList(gamesList)
        })

        model.rac_games.observe(viewLifecycleOwner, Observer { gamesList ->
            racAdapter.submitList(gamesList)
        })

        model.rpg_games.observe(viewLifecycleOwner, Observer { gamesList ->
            rpgAdapter.submitList(gamesList)
        })

        model.sig_games.observe(viewLifecycleOwner, Observer { gamesList ->
            sigAdapter.submitList(gamesList)
        })
        model.spo_games.observe(viewLifecycleOwner, Observer { gamesList ->
            spoAdapter.submitList(gamesList)
        })
        model.str_games.observe(viewLifecycleOwner, Observer { gamesList ->
            strAdapter.submitList(gamesList)
        })
    }

    private fun setViewPagerView(title : String, viewPagerAdapter: ViewPagerAdapter){
        val tv = TextView(context)
        tv.text = title
        tv.textSize = 18f
        tv.setTypeface(tv.typeface, Typeface.BOLD)

        val layoutParms = LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.WRAP_CONTENT,
            LinearLayout.LayoutParams.WRAP_CONTENT)
        layoutParms.setMargins(0,100,0,20)
        tv.layoutParams = layoutParms

        val vp = context?.let { ViewPager2(it) }
        vp?.let { setViewPager(it,viewPagerAdapter) }

        hBinding.linearLayout.addView(tv)
        hBinding.linearLayout.addView(vp)
    }

    private fun setMainViewPager(){
        // mainViewPager ?????? (Refactoring ??????)
        mainViewPagerAdapter = MainViewPagerAdapter()
        mainViewPagerAdapter.setOnItemClickListener(object : MainViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(context, GameActivity::class.java).apply {
                    putExtra("game",game)
                    putExtra("backFragment",R.id.first)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // ???????????? ( SDK ????????? ????????? ??????????????? ???????????? ?????????. )
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
        hBinding.mainViewPager.adapter = mainViewPagerAdapter
    }

    // viewPager ?????? ??????
    private fun setViewPager(viewPager: ViewPager2,viewPagerAdapter: ViewPagerAdapter){
        // ??????, ????????? ?????? ??????
        var pageMarginPx = resources.getDimensionPixelOffset(R.dimen.viewPageMargin)
        var pagerWidth = resources.getDimensionPixelOffset(R.dimen.viewPageWidth)
        var screenWidth = resources.displayMetrics.widthPixels // ??????????????? ?????? ????????? ?????????
        var offsetPx = screenWidth - pageMarginPx - pagerWidth

        // Adapter Click Event
        viewPagerAdapter.setOnItemClickListener(object : ViewPagerAdapter.OnItemClickListener{
            override fun onItemClick(v: View, game: Game, pos: Int) {
                Intent(context, GameActivity::class.java).apply {
                    // intent ?????? ???????????? ????????? url ????????????
                    putExtra("game",game)
                    putExtra("backFragment",R.id.first)
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }.run {
                    // ???????????? ( SDK ????????? ????????? ??????????????? ???????????? ?????????. )
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
        viewPager.adapter = viewPagerAdapter
        viewPager.setPageTransformer { page, position -> page.translationX = position * -offsetPx }
        viewPager.offscreenPageLimit = 2 // ??? ?????? ???????????? ?????? ?????? ???????????????
        viewPager.orientation = ViewPager2.ORIENTATION_HORIZONTAL
    }
}