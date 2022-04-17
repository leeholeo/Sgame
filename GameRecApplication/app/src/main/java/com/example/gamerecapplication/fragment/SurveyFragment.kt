package com.example.gamerecapplication.fragment

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.view.animation.AnimationUtils
import androidx.core.view.isInvisible
import androidx.databinding.DataBindingUtil
import androidx.fragment.app.viewModels
import androidx.lifecycle.Observer
import com.example.gamerecapplication.R
import com.example.gamerecapplication.activity.MainActivity
import com.example.gamerecapplication.activity.ResultActivity
import com.example.gamerecapplication.databinding.FragmentSurveyBinding
import com.example.gamerecapplication.viewmodel.MainViewModel
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class SurveyFragment : Fragment() {
    // view Binding
    private lateinit var sBinding: FragmentSurveyBinding
    private val model: MainViewModel by viewModels()
    private val loadingDialogFragment by lazy { LottieDialogFragment() }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // 모든 액티비티에 공통적으로 필요한 코드
        sBinding = DataBindingUtil.inflate(inflater,R.layout.fragment_survey,container,false)
        activity?.let {
            sBinding.lifecycleOwner = this
            sBinding.viewModel = model
        }
        Log.d("SurveyFragment","SurveyFragment")
        subscribeObservers()

        setAnimation()
        return sBinding.root
    }

    private fun subscribeObservers() {
        model.surveyEnd.observe(viewLifecycleOwner, Observer {
            if(it){
                Log.d("Survet End", "설문조사 종료")
                showProgressDialog()
                val handler: Handler = Handler()
                handler.postDelayed({
                    hideProgressDialog() },
                    20000)
                model.surveyEnd.value = false
            }
        })

        model.recommendEnd.observe(viewLifecycleOwner, Observer {
            if(it){
                Log.d("Recommend End", "추천 종료")
                Intent(context, ResultActivity::class.java).apply {
                    Log.d("Game List : ", "${model.recommendGame.value}")
                    putExtra("gameList",model.recommendGame.value)
                }.run {
                    startActivity(this)
                }
                model.recommendEnd.value = false
            }
        })
    }

    private fun showProgressDialog() {
        if (!loadingDialogFragment.isAdded) {
            loadingDialogFragment.show(parentFragmentManager, "loader")
        }
    }

    private fun hideProgressDialog() {
        if (loadingDialogFragment.isAdded) {
            loadingDialogFragment.dismissAllowingStateLoss()
        }
    }

    fun setAnimation(){
        // 설문 시작 버튼
        sBinding.btn0.setOnClickListener {
            sBinding.layoutStart.isInvisible = true
            sBinding.layoutBtn.isInvisible = false
            sBinding.layoutText.isInvisible = false
            sBinding.layoutProgress.isInvisible = false
        }

        // Anim
        val translateLeftAnim = AnimationUtils.loadAnimation(context, R.anim.translate_left)
        val translateRightAnim = AnimationUtils.loadAnimation(context, R.anim.translate_right)

        // 애니메이션 실행
        model.showAnimation.observe(activity as MainActivity, Observer {
            it.getContentIfNotHandled()?.let {
                // 코루틴
                GlobalScope.launch {
                    delay(200)
                    sBinding.btn1.startAnimation(translateLeftAnim)
                    sBinding.btn2.startAnimation(translateLeftAnim)
                    sBinding.textNumber.startAnimation(translateLeftAnim)
                    sBinding.textTitle.startAnimation(translateLeftAnim)
                    delay(500)
                    sBinding.btn1.startAnimation(translateRightAnim)
                    sBinding.btn2.startAnimation(translateRightAnim)
                    sBinding.textNumber.startAnimation(translateRightAnim)
                    sBinding.textTitle.startAnimation(translateRightAnim)
                }
            }
        })
    }
}