package com.example.capstone.networking

import com.google.gson.annotations.SerializedName

data class PostResponse(
    @SerializedName("Confidence")
    val confidence: String?,
    @SerializedName("Name")
    val name: String?,
    @SerializedName("Detail")
    val detail : String?,
    @SerializedName("Treatment")
    val treatment : String?
)