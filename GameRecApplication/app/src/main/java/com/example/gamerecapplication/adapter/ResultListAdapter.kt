package com.example.gamerecapplication.adapter

import android.content.Context
import android.content.Intent
import android.os.SystemClock
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.gamerecapplication.R
import com.example.gamerecapplication.activity.GameActivity
import com.example.gamerecapplication.model.Game

class ResultListAdapter (val context: Context, val gameList: ArrayList<Game>) : BaseAdapter() {
    interface OnItemClickListener{
        fun onItemClick(v: View, data: Game, pos : Int)
    }
    private var listener : OnItemClickListener? = null
    fun setOnItemClickListener(listener : OnItemClickListener) {
        this.listener = listener
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup?): View {
        /* LayoutInflater는 item을 Adapter에서 사용할 View로 부풀려주는(inflate) 역할을 한다. */
        val view: View = LayoutInflater.from(context).inflate(R.layout.result_item, null)

        /* 위에서 생성된 view를 res-layout-main_lv_item.xml 파일의 각 View와 연결하는 과정이다. */
        val gameBackground = view.findViewById<ImageView>(R.id.gameBackground)
        val gameName = view.findViewById<TextView>(R.id.gameName)
        val gameShortdescription = view.findViewById<TextView>(R.id.gameShortdescription)

        /* ArrayList<Game>의 변수 game의 이미지와 데이터를 ImageView와 TextView에 담는다. */
        val game = gameList[position]
        var genres = ""
        var mLastClickTime : Long = 0

        for(i in 0 until game.genres.size){
            genres += "${game.genres.get(i).description}"
            if(i != game.genres.size - 1) genres += ", "
        }

        Glide.with(context)
            .load(game.header_image)
            .placeholder(R.drawable.game1)
            .into(gameBackground)

        gameName.text = game.name
        gameShortdescription.text = genres

        // click listener
        view.setOnClickListener{
            if(SystemClock.elapsedRealtime() - mLastClickTime > 1000) {
                if ( position != RecyclerView.NO_POSITION){
                    listener?.onItemClick(view,game,position)
                }
            }
            mLastClickTime = SystemClock.elapsedRealtime()
        }

        return view
    }

    override fun getItem(position: Int): Any = gameList[position]
    override fun getItemId(position: Int): Long = 0
    override fun getCount(): Int = gameList.size

}