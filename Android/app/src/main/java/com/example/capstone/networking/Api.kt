package com.example.capstone.networking


import okhttp3.MultipartBody
import retrofit2.Call
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part

interface Api {
    //    @GET("function-4")
//    fun getPosts(): Call<ArrayList<PostResponse>>
    @Multipart
    @POST("upload")
    fun postImageBase64(@Part("image") image_base64: String): Call<ArrayList<PostResponse>>

    @Multipart
    @POST("upload")
    fun postImageFile(@Part part: MultipartBody.Part): Call<ArrayList<PostResponse>>
}