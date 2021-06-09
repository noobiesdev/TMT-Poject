package com.example.capstone

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.view.View
import android.view.WindowManager
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import android.app.ActivityOptions as AndroidAppActivityOptions

class SplashScreen : AppCompatActivity(){
    private val delay: Int = 1500

    lateinit var topAnim: Animation
    lateinit var bottomAnim: Animation
    lateinit var image: ImageView
    lateinit var logo: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash_screen)

        topAnim = AnimationUtils.loadAnimation(this,R.anim.top_animation)
        bottomAnim = AnimationUtils.loadAnimation(this,R.anim.bottom_animation)

        image = findViewById(R.id.imageView)
        logo = findViewById(R.id.textView)

        image.setAnimation(topAnim)
        logo.setAnimation(bottomAnim)

        Handler().postDelayed({
            val intentToMain = Intent(this, MainActivity::class.java)
            val pairs: Pair<View, String>
            pairs = Pair<View, String>(image, "logo_image")

            startActivity(intentToMain)
            finish()
        }, delay.toLong())
    }

}