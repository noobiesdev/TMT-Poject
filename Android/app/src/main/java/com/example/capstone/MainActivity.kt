package com.example.capstone
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.drawable.BitmapDrawable
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.view.WindowManager
import android.widget.Button
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import java.util.jar.Manifest

class MainActivity : AppCompatActivity(), View.OnClickListener {
    lateinit var captureButton: Button
    lateinit var imageView: ImageView
    lateinit var uploadButton: Button

    companion object {
        private const val CAMERA_PERMISSION_CODE = 1
        private const val CAMERA = 2
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        captureButton = findViewById(R.id.btn_camera)
        uploadButton = findViewById(R.id.btn_upload)
        imageView = findViewById(R.id.imagePreview)

        captureButton.isEnabled = false

        if (ActivityCompat.checkSelfPermission(
                this,
                android.Manifest.permission.CAMERA
            ) != PackageManager.PERMISSION_GRANTED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(android.Manifest.permission.CAMERA),
                111
            )
        } else
            captureButton.isEnabled = true

        captureButton.setOnClickListener(this)
        uploadButton.setOnClickListener(this)

    }

    override fun onClick(v: View) {
        when (v.id) {
            R.id.btn_camera -> capturePicture()
            R.id.btn_upload -> sendPicture()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if(requestCode == 101)
        {
            var pic: Bitmap? = data?.getParcelableExtra<Bitmap>("data")
            imageView.setImageBitmap(pic)

        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 111 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
            captureButton.isEnabled = true
        }
    }

    private fun capturePicture() {
        var i = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        startActivityForResult(i, 101)
    }

    private fun sendPicture() {
        var bmp: Bitmap? = (imageView.getDrawable() as BitmapDrawable).bitmap
        val intent = Intent(this@MainActivity,
            DetailActivity::class.java)
        intent.putExtra("imageBitmap",bmp)
        startActivity(intent)
    }

}
