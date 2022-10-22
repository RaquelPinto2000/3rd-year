package com.example.beeincontrolapp;

import android.content.Context;
import android.content.DialogInterface;
import android.widget.AbsSpinner;

class Spinner extends AbsSpinner implements DialogInterface.OnClickListener {

    public Spinner(Context context) {
        super(context);
    }

    @Override
    public void onClick(DialogInterface dialog, int which) {

    }
}
