package com.example.gamerecapplication.adapter


import android.os.SystemClock
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.gamerecapplication.R
import com.example.gamerecapplication.model.Game

class SteamViewPagerAdapter(arrayList: ArrayList<Game>) : RecyclerView.Adapter<SteamViewPagerAdapter.ViewPagerHolder>() {
    companion object {
        const val ITEM_COUNT = 40
    }

    private var gameList: List<Game>? = null

    interface OnItemClickListener{
        fun onItemClick(v: View, data: Game, pos : Int)
    }
    private var listener : OnItemClickListener? = null
    fun setOnItemClickListener(listener : OnItemClickListener) {
        this.listener = listener
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) = ViewPagerHolder((parent))

    override fun getItemCount(): Int = ITEM_COUNT

    // viewPager 관련 구현은 여기서
    override fun onBindViewHolder(holder: ViewPagerHolder, position: Int) {
        gameList?.let { gameList->
            holder.bind(gameList[position])
        }
    }

    fun submitList(list: List<Game>?) {
        gameList = list
        notifyDataSetChanged()
    }

    inner class ViewPagerHolder(parent: ViewGroup) : RecyclerView.ViewHolder
        (LayoutInflater.from(parent.context).inflate(R.layout.main_list_item, parent, false)){
        val ivGame : ImageView = itemView.findViewById(R.id.gameImageView)
        val tvName : TextView = itemView.findViewById(R.id.textName)
        private var mLastClickTime : Long = 0

        fun bind(game : Game){
            tvName.text = game.name
            ivGame.clipToOutline = true
            Glide.with(itemView)
                .load(game.header_image)
                .override(itemView.resources.getDimension(R.dimen.viewPageWidth).toInt())
                .into(ivGame)

            ivGame.setOnClickListener {
                if(SystemClock.elapsedRealtime() - mLastClickTime > 1000) {
                    val pos = adapterPosition
                    if ( pos != RecyclerView.NO_POSITION){
                        listener?.onItemClick(itemView,game,pos)
                        Log.d("viewPager" ,"${tvName.text} ${ivGame.transitionName}")
                    }
                }
                mLastClickTime = SystemClock.elapsedRealtime()
            }
        }
    }
}