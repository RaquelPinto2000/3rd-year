package com.example.beeincontrolapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

public class SignIn extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.sign_in_page);
    }

    public void LoginDone(View view) {
        startActivity(new Intent(this, Apiaries.class));
    }
    public void GoLogin(View view){ startActivity(new Intent(this, MainActivity.class)); }
}
