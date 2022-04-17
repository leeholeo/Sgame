package com.example.gamerecapplication.activity

import android.content.Intent
import android.content.SharedPreferences
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.widget.Toast
import com.example.gamerecapplication.R
import com.example.gamerecapplication.databinding.ActivityLoginBinding
import com.example.gamerecapplication.model.*
import com.example.gamerecapplication.service.GamesService
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInAccount
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.GoogleAuthProvider
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class LoginActivity : AppCompatActivity(){
    lateinit var LBinding : ActivityLoginBinding
    lateinit var pref : SharedPreferences
    lateinit var editor : SharedPreferences.Editor

    //구글 로그인
    //firebase Auth
    private lateinit var firebaseAuth: FirebaseAuth
    //google client
    private lateinit var googleSignInClient: GoogleSignInClient
    //private const val TAG = "GoogleActivity"
    private val RC_SIGN_IN = 99

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        LBinding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(LBinding.root)

//        // 1. Shared Preference 초기화
//        pref = getPreferences(Context.MODE_PRIVATE)
//        editor = pref.edit()
//
//        // 2. 레이아웃 변수 초기화
//        // 3. 저장해둔 값 불러오기 -> 저장된 값이 없으면 "" 로 들고옴
//        var inputData = pref.getString("InputData","")
//
//        // 4. 앱을 새로 켜면 이전에 저장해둔 값이 표시됨
//        LBinding.edtId.setText(inputData.toString())
//
//        // 5. 각 버튼 클릭시 새로운 값 저장
//        LBinding.btnSave.setOnClickListener(View.OnClickListener {
//            // (key : InputData, value : EditText에 입력한 데이터)
//            editor.putString("InputData",LBinding.edtId.text.toString())
//            editor.apply()
//        })

        //구글 로그인
        LBinding.btnGoogleSignIn.setOnClickListener {signIn()}
        //게스트 로그인
        LBinding.btnGuestSignIn.setOnClickListener {guestSignIn()}

        //Google 로그인 옵션 구성. requestIdToken 및 Email 요청
        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(R.string.default_web_client_id))
            .requestEmail()
            .build()

        googleSignInClient = GoogleSignIn.getClient(this, gso)

        //firebase auth 객체
        firebaseAuth = FirebaseAuth.getInstance()
    }

    // onStart. 유저가 앱에 이미 구글 로그인을 했는지 확인
    public override fun onStart() {
        super.onStart()
        val account = GoogleSignIn.getLastSignedInAccount(this)
        if(account!==null){ // 이미 로그인 되어있을시 바로 메인 액티비티로 이동
            Log.d("onStart ", "현재 로그인되어 있으므로 이동")
            toMainActivity(firebaseAuth.currentUser)
        }
        if(firebaseAuth.currentUser != null){
            toMainActivity(firebaseAuth.currentUser)
        }
    } //onStart End

    // onActivityResult
    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        // Result returned from launching the Intent from GoogleSignInApi.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN) {
            val task = GoogleSignIn.getSignedInAccountFromIntent(data)
            try {
                // Google Sign In was successful, authenticate with Firebase
                val account = task.getResult(ApiException::class.java)
                firebaseAuthWithGoogle(account!!)
            } catch (e: ApiException) {
                // Google Sign In failed, update UI appropriately
                Log.w("LoginActivity", "Google sign in failed", e)
            }
        }
    } // onActivityResult End

    // firebaseAuthWithGoogle
    private fun firebaseAuthWithGoogle(acct: GoogleSignInAccount) {
        Log.d("LoginActivity", "firebaseAuthWithGoogle:" + acct.id!!)

        //Google SignInAccount 객체에서 ID 토큰을 가져와서 Firebase Auth로 교환하고 Firebase에 인증
        val credential = GoogleAuthProvider.getCredential(acct.idToken, null)
        firebaseAuth.signInWithCredential(credential)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    Log.w("LoginActivity", "firebaseAuthWithGoogle 성공", task.exception)
                    postApp(firebaseAuth?.currentUser)
                    toMainActivity(firebaseAuth?.currentUser)
                } else {
                    Log.w("LoginActivity", "firebaseAuthWithGoogle 실패", task.exception)
                    //Snackbar.make(login_layout, "로그인에 실패하였습니다.", Snackbar.LENGTH_SHORT).show()
                }
            }
    }// firebaseAuthWithGoogle END

    // toMainActivity
    fun toMainActivity(user: FirebaseUser?) {
        if(user !=null) { // MainActivity 로 이동
            startActivity(Intent(this, MainActivity::class.java))
            finish()
        }
    } // toMainActivity End

    // signIn
    private fun signIn() {
        val signInIntent = googleSignInClient.signInIntent
        startActivityForResult(signInIntent, RC_SIGN_IN)
    }
    // signIn End

    //익명 로그인
    private fun guestSignIn(){
        firebaseAuth.signInAnonymously()
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    // Sign in success, update UI with the signed-in user's information
                    Log.d("success", "signInAnonymously:success")
                    val user = firebaseAuth.currentUser
                    val intent = Intent(this, MainActivity::class.java)
                    intent.putExtra("uid",user!!.uid)
                    postApp(firebaseAuth?.currentUser)
                    startActivity(intent)
                    finish()
                    //updateUI(user)
                } else {
                    // If sign in fails, display a message to the user.
                    Log.w("failure", "signInAnonymously:failure", task.exception)
                    Toast.makeText(baseContext, "Authentication failed.",
                        Toast.LENGTH_SHORT).show()
                    //updateUI(null)
                }
            }
    }

    fun postApp(user: FirebaseUser?){
        CoroutineScope(Dispatchers.Main).launch {
            val gameService = GamesService.getGamesService()
            val uid = user?.uid?:"none"

            val response = gameService.getApp(uid)

            if(response.code() == 404){
                // User 정보 초기화
                val app = App(uid)
                gameService.createApp(app)

                // Favorite 초기화
                val favorite = Favorite(uid,ArrayList())
                gameService.createFavorite(favorite)

                // SurvetResult 초기화
                val surveyResult = SurveyAnswerResult(uid,ArrayList())
                gameService.createSurveyResult(surveyResult)
            }
        }
    }
}