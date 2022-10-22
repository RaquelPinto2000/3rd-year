package com.example.beeincontrolapp;

import android.app.ActionBar;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;

import androidx.appcompat.app.AppCompatActivity;

public class Beehives extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.beehives_main);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

    }
    public void SeeTasks(View view) { startActivity(new Intent(this, Tasks.class)); }
    public void SeeBeehive(View view) { startActivity(new Intent(this, BeehivesTable.class));}
    public void SeeBeehive2(View view) { startActivity(new Intent(this, BeehivesTable2.class));}
    public void SeeBeehive3(View view) {
        startActivity(new Intent(this, BeehivesTable3.class));
    }
    public void SeeReports(View view) { startActivity(new Intent(this, Reports.class)); }
    public void addBeehive(View view) { startActivity(new Intent(this, AddBeehive.class)); }

    //menu das 3 pintas
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        return super.onOptionsItemSelected(item);
    }

    public void Setting(MenuItem menuItem) {
        Intent Reportintent = new Intent(this, Settings.class);
        startActivity(Reportintent);
    }
    public void Help(MenuItem menuItem) {
        Intent Reportintent = new Intent(this, help.class);
        startActivity(Reportintent);
    }
    public void Sign_Out(MenuItem menuItem) {
        Intent Reportintent = new Intent(this, MainActivity.class);
        startActivity(Reportintent);
    }



}
