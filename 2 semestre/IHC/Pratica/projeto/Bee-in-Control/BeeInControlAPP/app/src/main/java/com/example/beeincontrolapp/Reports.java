package com.example.beeincontrolapp;

import android.app.ActionBar;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

import com.anychart.AnyChart;
import com.anychart.AnyChartView;
import com.anychart.chart.common.dataentry.DataEntry;
import com.anychart.chart.common.dataentry.ValueDataEntry;
import com.anychart.charts.Pie;

import java.util.ArrayList;
import java.util.List;

public class Reports extends AppCompatActivity {
    AnyChartView anychart;
    String[] beeh = {"Foxtrot", "Lusitana", "Reversível"};
    int[] x = {500, 800, 2000};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.reports_page);
        anychart = findViewById(R.id.any_chart_view);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        setupPieChart();
    }
    public void setupPieChart(){
        Pie pie = AnyChart.pie();
        List<DataEntry> dataEntries = new ArrayList<>();
        for (int i = 0; i < beeh.length; i++){
            dataEntries.add(new ValueDataEntry(beeh[i], x[i]));

        }
        pie.data(dataEntries);
        anychart.setChart(pie);
    }

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
