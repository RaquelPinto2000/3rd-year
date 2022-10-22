package com.example.beeincontrolapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

public class AddBeehive extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.add_beehive);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
    }

    public void cancelAndBack(View view) { startActivity(new Intent(this, Beehives.class)); }

    public void hideText1(View view) {
        EditText t = (EditText)findViewById(R.id.editTextTextPersonName9);
        t.setText("");
    }
    public void hideText2(View view) {
        EditText t = (EditText)findViewById(R.id.editTextTextPersonName10);
        t.setText("");
    }
    public void hideText3(View view) {
        EditText t = (EditText)findViewById(R.id.editTextTextPersonName11);
        t.setText("");
    }
    public void hideText4(View view) {
        EditText t = (EditText)findViewById(R.id.editTextTextPersonName13);
        t.setText("");
    }

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
