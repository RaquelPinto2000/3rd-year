package com.example.beeincontrolapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

public class Apiaries extends AppCompatActivity {
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


    //resto da pagina
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.nav_activity_main);
    }
    public void ChooseApiary(View view) { startActivity(new Intent(this, Beehives.class)); }

    public void AddApiary(View view) { startActivity(new Intent(this, AddApiary.class)); }

    public void sortByAlcas(View view) { startActivity(new Intent(this, AddApiary.class)); }

    public void goToApiaries(MenuItem item) { startActivity(new Intent(this, Apiaries.class)); }

    public void goToAllTasks(MenuItem item) { startActivity(new Intent(this, AllTasks.class)); }

    public void goToReports(MenuItem item) { startActivity(new Intent(this, Reports.class)); }

    public void goToApiary1(View view) { startActivity(new Intent(this, Beehives.class)); }

    public void goToApiary2(View view) { startActivity(new Intent(this, Beehives2.class)); }

    public void goToApiary3(View view) { startActivity(new Intent(this, Beehives3.class)); }


}
