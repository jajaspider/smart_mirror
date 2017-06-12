package com.example.how32.scheduleapplication;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class AddScheduleActivity extends AppCompatActivity {

    private static final int CONNECTION_TIME = 5000;

    private String date = null;
    private String time = null;
    private String subject = null;

    private String dateTime = null;

    EditText dateText = null;
    EditText timeText = null;
    EditText subjectText  = null;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_schedule);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        dateText = (EditText)findViewById(R.id.schedule_date);
        timeText = (EditText)findViewById(R.id.schedule_Time);
        subjectText = (EditText)findViewById(R.id.schedule_Subject);

    }

    public void onClick(View v) {
        switch(v.getId()) {
            case R.id.b_insert :
                date = dateText.getText().toString();
                time = timeText.getText().toString();
                subject = subjectText.getText().toString();

                dateTime = date + "" + time;
                dataInsert("http://finite.servegame.com:25565/schedule_dbinsert.php", dateTime, subject);
                break;
        }
    }
    private void dataInsert(String url, String dateTime, String subject) {
        class PHPInsert extends AsyncTask<String, Integer, String> {

            @Override
            protected String doInBackground(String... params) {
                //파라미터 1 : url, 2 : dateTime, 3 : subject
                String result = null;
                String data = "p_date=" + params[1] + "&p_subject=" + params[2];
                try {
                    URL url = new URL(params[0]);
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setDoOutput(true);
                    conn.setDoInput(true);
                    if (conn != null) {
                        //연결시작되면
                        conn.setConnectTimeout(CONNECTION_TIME);
                        conn.setUseCaches(false);
                        //데이터 입력 후 전송
                        OutputStream outputStream = conn.getOutputStream();
                        outputStream.write(data.getBytes("UTF-8"));
                        outputStream.flush();
                        outputStream.close();
                        //if (conn.getResponseCode() == HttpURLConnection.HTTP_OK) {
                        //연결 성공 시 실행
                        BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                        result = reader.readLine();
                        Log.w("result" , result);
                        //읽어온 데이터를 저장함
                        conn.disconnect();
                    }
                    return result;
                } catch (Exception e) {
                    return null;
                }
            }

            @Override
            protected void onPostExecute(String s) {
                super.onPostExecute(s);
                Toast.makeText(AddScheduleActivity.this, s, Toast.LENGTH_SHORT).show();
            }
        }

        PHPInsert phpInsert = new PHPInsert();
        phpInsert.execute(url, dateTime, subject);
    }
}
