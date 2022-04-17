package com.example.gamerecapplication.adapter

import android.app.Dialog
import android.os.SystemClock
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.gamerecapplication.R
import com.example.gamerecapplication.model.Screenshot

class ScreenShotViewPagerAdapter(list: ArrayList<Screenshot>) : RecyclerView.Adapter<ScreenShotViewPagerAdapter.ScreenShotViewPagerHolder>() {
    var item = list

    interface OnItemClickListener{
        fun onItemClick(v: View, data: String, pos : Int)
    }
    private var listener : OnItemClickListener? = null
    fun setOnItemClickListener(listener : OnItemClickListener) {
        this.listener = listener
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = ScreenShotViewPagerHolder((parent))

    override fun getItemCount(): Int = item.size

    // viewPager 관련 구현은 여기서
    override fun onBindViewHolder(holder: ScreenShotViewPagerHolder, position: Int) {
        holder.bind(item[position].path_thumbnail)
    }

    inner class ScreenShotViewPagerHolder(parent: ViewGroup) : RecyclerView.ViewHolder
        (LayoutInflater.from(parent.context).inflate(R.layout.screenshot_list_item, parent, false)){
        val ivGame : ImageView = itemView.findViewById(R.id.scrrenShotImageView)
        private var mLastClickTime : Long = 0

        fun bind(url : String){
            ivGame.clipToOutline = true
            Glide.with(itemView)
                .load(url)
                .override(itemView.resources.getDimension(R.dimen.viewPageWidth).toInt())
                .into(ivGame)

            ivGame.setOnClickListener {
                if(SystemClock.elapsedRealtime() - mLastClickTime > 1000) {
                    val pos = adapterPosition
                    if ( pos != RecyclerView.NO_POSITION){
                        listener?.onItemClick(ivGame,url,pos)
                    }
                }
                mLastClickTime = SystemClock.elapsedRealtime()
            }
        }
    }
}