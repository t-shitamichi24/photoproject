from django.shortcuts import render
# django.views.genericからTemplateView、ListViewをインポート
from django.views.generic import TemplateView, ListView
# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost
# django.views.genericからDetailViewをインポート
from django.views.generic import DetailView
# django.views.genericからDeleteViewをインポート
from django.views.generic import DeleteView

class IndexView(ListView):
    '''トップページのビュー
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # モデルBlogPostのオブジェクトにorder_by()を適用して
    # 投稿日時の降順で並べ替える
    queryset = PhotoPost.objects.order_by('-posted_at')
    # 1ページに表示するレコードの件数
    paginate_by = 9

# デコレーターにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページのビュー
    
    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する
    
    Attributes:
      form_class: モデルとフィールドが登録されたフォームクラス
      template_name: レンダリングするテンプレート
      success_url: データベスへの登録完了後のリダイレクト先
    '''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = "post_photo.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録をここで行う
        
        parameters:
          form(django.forms.Form):
            form_classに格納されているPhotoPostFormオブジェクト
        Return:
          HttpResponseRedirectオブジェクト:
            スーパークラスのform_valid()の戻り値を返すことで、
            success_urlで設定されているURLにリダイレクトさせる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    
    Attributes:
      template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name ='post_success.html'

class CategoryView(ListView):
    '''カテゴリページのビュー
    
    Attributes:
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
      '''クエリを実行する
      
      self.kwargsの取得が必要なため、クラス変数querysetではなく、
      get_queryset（）のオーバーライドによりクエリを実行する
      
      Returns:
        クエリによって取得されたレコード
      '''     
      # self.kwargsでキーワードの辞書を取得し、
      # categoryキーの値(Categorysテーブルのid)を取得
      category_id = self.kwargs['category']
      # filter(フィールド名=id)で絞り込む
      categories = PhotoPost.objects.filter(
        category=category_id).order_by('-posted_at')
      # クエリによって取得されたレコードを返す
      return categories

class UserView(ListView):
    '''ユーザーの投稿一覧ページのビュー
    
    Attributes:
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
      '''クエリを実行する
      
      self.kwargsの取得が必要なため、クラス変数querysetではなく、
      get_queryset（）のオーバーライドによりクエリを実行する
      
      Returns:
        クエリによって取得されたレコード
      '''
      # self.kwargsでキーワードの辞書を取得し、
      # userキーの値(ユーザーテーブルのid)を取得
      user_id = self.kwargs['user']
      # filter(フィールド名=id)で絞り込む
      user_list = PhotoPost.objects.filter(
        user=user_id).order_by('-posted_at')
      # クエリによって取得されたレコードを返す
      return user_list

class DetailView(DetailView):
    '''詳細ページのビュー
    
    投稿記事の詳細を表示するのでDetailViewを継承する
     Attributes:
      template_name: レンダリングするテンプレート
      model: モデルのクラス
    '''
    # post.htmlをレンダリングする
    template_name ='detail.html'
    # クラス変数modelにモデルBlogPostを設定
    model = PhotoPost

class MypageView(ListView):
    '''マイページのビュー
    
    Attributes:
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
    '''
    # mypage.htmlをレンダリングする
    template_name ='mypage.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
      '''クエリを実行する
      
      self.kwargsの取得が必要なため、クラス変数querysetではなく、
      get_queryset（）のオーバーライドによりクエリを実行する
      
      Returns:
        クエリによって取得されたレコード
      '''
      # 現在ログインしているユーザー名はHttpRequest.userに格納されている
      # filter(userフィールド=userオブジェクト)で絞り込む
      queryset = PhotoPost.objects.filter(
        user=self.request.user).order_by('-posted_at')
      # クエリによって取得されたレコードを返す
      return queryset
  
class PhotoDeleteView(DeleteView):
    '''レコードの削除を行うビュー
    
    Attributes:
      model: モデル
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
      success_url: 削除完了後のリダイレクト先のURL
    '''
    # 操作の対象はPhotoPostモデル
    model = PhotoPost
    # photo_delete.htmlをレンダリングする
    template_name ='photo_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('photo:mypage')

    def delete(self, request, *args, **kwargs):
      '''レコードの削除を行う
      
      Parameters:
        self: PhotoDeleteViewオブジェクト
        request: WSGIRequest(HttpRequest)オブジェクト
        args: 引数として渡される辞書(dict)
        kwargs: キーワード付きの辞書(dict)
                {'pk': 21}のようにレコードのidが渡される
      
      Returns:
        HttpResponseRedirect(success_url)を返して
        success_urlにリダイレクト
      '''
      # スーパークラスのdelete()を実行
      return super().delete(request, *args, **kwargs)