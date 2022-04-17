package com.example.gamerecapplication.activity

import android.os.Bundle
import android.util.Log
import android.widget.TextView
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.Fragment
import androidx.fragment.app.FragmentManager
import androidx.fragment.app.FragmentTransaction
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.example.gamerecapplication.viewmodel.MainViewModel
import com.example.gamerecapplication.R
import com.example.gamerecapplication.databinding.ActivityMainBinding
import com.example.gamerecapplication.fragment.HomeFragment
import com.example.gamerecapplication.fragment.MypageFragment
import com.example.gamerecapplication.fragment.SurveyFragment

private const val HOME_FRAGMENT = "home_fragment"
private const val SURVEY_FRAGMENT = "survey_fragment"
private const val MYPAGE_FRAGMENT = "mypage_fragment"

class MainActivity : AppCompatActivity() {
    // view Binding
    private lateinit var mBinding: ActivityMainBinding
    private val model: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        // 모든 액티비티에 공통적으로 필요한 코드
        super.onCreate(savedInstanceState)
        mBinding = DataBindingUtil.setContentView(this, R.layout.activity_main)
        mBinding.lifecycleOwner = this
        mBinding.viewModel = model

        setBottomNavigation()
    }

    // OnNavigationItemSelectedListener를 통해 탭 아이템 선택 시 이벤트를 처리
    fun setBottomNavigation(){
        // navi_menu.xml 에서 설정했던 각 아이템들의 id를 통해 알맞은 프래그먼트로 변경하게 한다.
        mBinding.bnvMain.run { setOnItemSelectedListener  {
            when(it.itemId) {
                //프래그먼트 빠르게
                R.id.first -> {
                    setFragment(HOME_FRAGMENT, HomeFragment())
                    //supportFragmentManager.beginTransaction().replace(R.id.fl_container, HomeFragment()).commit()
                    mBinding.bnvMain.itemIconTintList = ContextCompat.getColorStateList(context, R.color.color_bnv)
                    mBinding.bnvMain.itemTextColor = ContextCompat.getColorStateList(context, R.color.color_bnv)
                }
                R.id.second -> {
                    setFragment(SURVEY_FRAGMENT, SurveyFragment())
                    //supportFragmentManager.beginTransaction().replace(R.id.fl_container, SurveyFragment()).commit()
                    mBinding.bnvMain.itemIconTintList = ContextCompat.getColorStateList(context, R.color.color_bnv)
                    mBinding.bnvMain.itemTextColor = ContextCompat.getColorStateList(context, R.color.color_bnv)
                }
                R.id.third -> {
                    setFragment(MYPAGE_FRAGMENT, MypageFragment())
                    //supportFragmentManager.beginTransaction().replace(R.id.fl_container, mypageFragment).commit()
                    mBinding.bnvMain.itemIconTintList = ContextCompat.getColorStateList(context, R.color.color_bnv)
                    mBinding.bnvMain.itemTextColor = ContextCompat.getColorStateList(context, R.color.color_bnv)
                }
            }
            true
        }
            selectedItemId = intent.getIntExtra("backFragment",R.id.first) // 앱 실행시 보일 fragment
        }
    }

    /* Fragment State 유지 함수 */
    private fun setFragment(tag: String, fragment: Fragment) {
        val manager: FragmentManager = supportFragmentManager
        val ft: FragmentTransaction = manager.beginTransaction()

        if (manager.findFragmentByTag(tag) == null) {
            ft.add(R.id.fl_container, fragment, tag)
        }

        val home = manager.findFragmentByTag(HOME_FRAGMENT)
        val survey = manager.findFragmentByTag(SURVEY_FRAGMENT)
        val mypage = manager.findFragmentByTag(MYPAGE_FRAGMENT)

        // Hide all Fragment
        if (home != null) {
            ft.hide(home)
        }
        if (survey != null) {
            ft.hide(survey)
        }
        if (mypage != null) {
            ft.hide(mypage)
        }

        // Show  current Fragment
        if (tag == HOME_FRAGMENT) {
            if (home != null) {
                ft.show(home)
            }
        }
        if (tag == SURVEY_FRAGMENT) {
            if (survey != null) {
                ft.show(survey)
            }
        }
        if (tag == MYPAGE_FRAGMENT) {
            if (mypage != null) {
                ft.show(mypage)
            }
        }
        ft.commitAllowingStateLoss()
    }
}