package com.example.capstone

import android.content.Intent
import android.graphics.Bitmap
import android.media.Image
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.capstone.networking.PostAdapter
import com.example.capstone.networking.PostResponse
import com.example.capstone.networking.RetrofitClient
import com.example.capstone.util.ImageUtil
import okhttp3.MediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Call
import retrofit2.Response
import java.io.ByteArrayOutputStream


class DetailActivity :AppCompatActivity(),View.OnClickListener{
    lateinit var rvPost: RecyclerView
    lateinit var tvResponseCode: TextView
    lateinit var imageView : ImageView
    lateinit var mainmenuButton: Button

    private val list = ArrayList<PostResponse>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detail)

        rvPost = findViewById(R.id.rvPost)
        tvResponseCode = findViewById(R.id.tvResponseCode)
        imageView = findViewById(R.id.imagePreview)
        mainmenuButton = findViewById(R.id.btn_main_menu)

        mainmenuButton.setOnClickListener(this)

//        Receive ImageBitMap from Previous Activity and Display it
        val bundle: Bundle? = intent?.extras
        val imageBitmap : Bitmap? = bundle?.get("imageBitmap") as Bitmap?
        imageView.setImageBitmap(imageBitmap)

        rvPost.setHasFixedSize(true)
        rvPost.layoutManager = LinearLayoutManager(this)
//        uploadPictureAsBase64(imageBitmap)
        uploadPictureAsBytesArray(imageBitmap)
//
//        RetrofitClient.instance.getPosts().enqueue(object: retrofit2.Callback<ArrayList<PostResponse>>{
//            override fun onFailure(call: Call<ArrayList<PostResponse>>, t: Throwable) {
//
//            }
//
//            override fun onResponse(
//                call: Call<ArrayList<PostResponse>>,
//                response: Response<ArrayList<PostResponse>>
//            ) {
//                val responseCode = response.code().toString()
//                tvResponseCode.text = responseCode
//                response.body()?.let { list.addAll(it) }
//                val adapter = PostAdapter(list)
//                rvPost.adapter = adapter
//            }
//
//
//        })

    }

    private fun uploadPictureAsBase64(imageBitMap: Bitmap?){

//        Bitmap to base64
        val base64String: String = ImageUtil().convert(imageBitMap)
        println("Finished Convert")
        RetrofitClient.instance.postImageBase64(base64String).enqueue(object: retrofit2.Callback<ArrayList<PostResponse>>{
            override fun onFailure(call: Call<ArrayList<PostResponse>>, t:Throwable){
                println("Failure")
                println(t.message)
//                println(t.message.toString())
            }
            override fun onResponse(
                call: Call<ArrayList<PostResponse>>,
                response: Response<ArrayList<PostResponse>>
            ) {
                val responseCode = response.code().toString()
                tvResponseCode.text = responseCode
                response.body()?.let { list.addAll(it) }
                val adapter = PostAdapter(list)
                rvPost.adapter = adapter
            }
        })
    }

    private fun uploadPictureAsBytesArray(imageBitMap: Bitmap?){

        val imageOutStream: ByteArrayOutputStream = ImageUtil().asByteArrayOutputStream(imageBitMap)
        val part = MultipartBody.Part.createFormData(
            "image", "uploaded_image.png", RequestBody.create(
                MediaType.parse("image/*"), imageOutStream.toByteArray()
            )
        )

        RetrofitClient.instance.postImageFile(part).enqueue(object: retrofit2.Callback<ArrayList<PostResponse>>{
            override fun onFailure(call: Call<ArrayList<PostResponse>>, t:Throwable){
                println("Failure")
                println(t.message)
//                println(t.message.toString())
            }
            override fun onResponse(
                call: Call<ArrayList<PostResponse>>,
                response: Response<ArrayList<PostResponse>>
            ) {
                val responseCode = response.code().toString()
                tvResponseCode.text = responseCode
                response.body()?.let { list.addAll(it) }
                val adapter = PostAdapter(list)
                rvPost.adapter = adapter
            }
        })
    }

    override fun onClick(v: View) {
        when (v.id) {
            R.id.btn_main_menu -> mainMenu()
        }
    }
    private fun mainMenu() {
        val intent = Intent(this,
            MainActivity::class.java)
        startActivity(intent)
    }
}