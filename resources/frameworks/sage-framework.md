# Sage Framework

Comprehensive guide to Sage Framework - modern WordPress development with Blade templating and Laravel components.

## Sage Fundamentals

### Installation and Setup

```bash
# Install Sage via Composer
composer create-project roots/sage your-theme-name

# Or install via WP-CLI
wp scaffold _s your-theme-name --theme_name="Your Theme Name" --author="Your Name"

# Navigate to theme directory
cd your-theme-name

# Install dependencies
composer install
npm install
```

### Sage Configuration

```php
// config/app.php - Main configuration file
return [
    'name' => 'Sage Theme',
    'slug' => 'sage-theme',
    'version' => '1.0.0',
    'description' => 'A modern WordPress theme built with Sage',
    'author' => 'Your Name',
    'author_uri' => 'https://example.com',
    'domain' => 'sage-theme',
    
    // Asset configuration
    'assets' => [
        'manifest' => 'dist/assets.json',
        'dist' => 'dist',
    ],
    
    // Blade configuration
    'blade' => [
        'directories' => [
            'resources/views',
        ],
        'cache' => WP_DEBUG ? false : 'cache/blade',
    ],
    
    // Service providers
    'providers' => [
        App\Providers\ThemeServiceProvider::class,
        App\Providers\AssetServiceProvider::class,
        App\Providers\BladeServiceProvider::class,
    ],
];
```

### Basic Sage Structure

```php
// app/setup.php - Theme setup
namespace App;

use function Roots\bundle;

class Setup {
    
    public function __construct() {
        add_action('after_setup_theme', [$this, 'themeSupport']);
        add_action('wp_enqueue_scripts', [$this, 'enqueueAssets']);
        add_action('widgets_init', [$this, 'registerWidgets']);
    }
    
    public function themeSupport() {
        // Theme support
        add_theme_support('post-thumbnails');
        add_theme_support('title-tag');
        add_theme_support('html5', [
            'comment-list',
            'comment-form',
            'search-form',
            'gallery',
            'caption',
        ]);
        
        // Custom logo
        add_theme_support('custom-logo', [
            'height' => 100,
            'width' => 400,
            'flex-height' => true,
            'flex-width' => true,
        ]);
        
        // Custom background
        add_theme_support('custom-background', [
            'default-color' => 'ffffff',
        ]);
    }
    
    public function enqueueAssets() {
        // Enqueue Sage assets
        bundle('app')->enqueue();
        
        // Localize script
        wp_localize_script('app', 'sage', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('sage_nonce'),
        ]);
    }
    
    public function registerWidgets() {
        register_sidebar([
            'name' => __('Primary Sidebar', 'sage-theme'),
            'id' => 'primary-sidebar',
            'description' => __('Add widgets here.', 'sage-theme'),
            'before_widget' => '<section id="%1$s" class="widget %2$s">',
            'after_widget' => '</section>',
            'before_title' => '<h2 class="widget-title">',
            'after_title' => '</h2>',
        ]);
    }
}

new Setup();
```

## Blade Templating

### Basic Blade Syntax

```blade
{{-- resources/views/base.blade.php --}}
<!DOCTYPE html>
<html {!! get_language_attributes() !!}>
<head>
    <meta charset="{!! get_bloginfo('charset') !!}">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    
    @php wp_head() @endphp
</head>

<body {!! body_class() !!}>
    <div id="page" class="site">
        <a class="skip-link screen-reader-text" href="#primary">Skip to content</a>

        @include('partials.header')

        <main id="primary" class="site-main">
            @yield('content')
        </main>

        @include('partials.footer')
    </div>

    @php wp_footer() @endphp
</body>
</html>
```

### Blade Components and Layouts

```blade
{{-- resources/views/partials/header.blade.php --}}
<header id="masthead" class="site-header">
    <div class="container">
        <div class="site-branding">
            @if(has_custom_logo())
                {!! get_custom_logo() !!}
            @else
                <h1 class="site-title">
                    <a href="{!! home_url('/') !!}" rel="home">{!! get_bloginfo('name') !!}</a>
                </h1>
                @if(get_bloginfo('description'))
                    <p class="site-description">{!! get_bloginfo('description') !!}</p>
                @endif
            @endif
        </div>

        <nav id="site-navigation" class="main-navigation">
            @if(has_nav_menu('primary'))
                {!! wp_nav_menu([
                    'theme_location' => 'primary',
                    'menu_id' => 'primary-menu',
                    'container' => false,
                    'menu_class' => 'nav-menu',
                    'fallback_cb' => false,
                ]) !!}
            @endif
        </nav>
    </div>
</header>
```

### Template Inheritance

```blade
{{-- resources/views/index.blade.php --}}
@extends('base')

@section('content')
    <div class="posts-container">
        @if(have_posts())
            @while(have_posts())
                @php the_post() @endphp
                
                <article @php post_class() @endphp>
                    <header class="entry-header">
                        @if(has_post_thumbnail())
                            <div class="post-thumbnail">
                                <a href="{!! get_permalink() !!}">
                                    {!! get_the_post_thumbnail(null, 'medium') !!}
                                </a>
                            </div>
                        @endif
                        
                        <h2 class="entry-title">
                            <a href="{!! get_permalink() !!}" rel="bookmark">{!! get_the_title() !!}</a>
                        </h2>
                        
                        <div class="entry-meta">
                            <span class="posted-on">
                                <time class="entry-date published" datetime="{!! get_the_date('c') !!}">
                                    {!! get_the_date() !!}
                                </time>
                            </span>
                            <span class="byline">
                                {!! __('by', 'sage-theme') !!}
                                <span class="author vcard">
                                    <a class="url fn n" href="{!! get_author_posts_url(get_the_author_meta('ID')) !!}">
                                        {!! get_the_author() !!}
                                    </a>
                                </span>
                            </span>
                        </div>
                    </header>

                    <div class="entry-content">
                        {!! get_the_excerpt() !!}
                        <a href="{!! get_permalink() !!}" class="read-more">
                            {!! __('Continue reading', 'sage-theme') !!}
                        </a>
                    </div>

                    <footer class="entry-footer">
                        <span class="cat-links">
                            {!! __('Posted in', 'sage-theme') !!} {!! get_the_category_list(', ') !!}
                        </span>
                        
                        @if(get_comments_number() > 0)
                            <span class="comments-link">
                                <a href="{!! get_comments_link() !!}">
                                    {!! get_comments_number() !!} {!! __('Comments', 'sage-theme') !!}
                                </a>
                            </span>
                        @endif
                    </footer>
                </article>
            @endwhile
            
            @if(get_the_posts_navigation())
                {!! get_the_posts_navigation() !!}
            @endif
        @else
            <p>{!! __('Sorry, no posts found.', 'sage-theme') !!}</p>
        @endif
    </div>
@endsection
```

## Sage Components

### Custom Blade Components

```php
// app/View/Components/PostCard.php
namespace App\View\Components;

use Illuminate\View\Component;

class PostCard extends Component {
    
    public $post;
    public $showExcerpt;
    public $showMeta;
    
    public function __construct($post = null, $showExcerpt = true, $showMeta = true) {
        $this->post = $post ?: get_post();
        $this->showExcerpt = $showExcerpt;
        $this->showMeta = $showMeta;
    }
    
    public function render() {
        return view('components.post-card');
    }
}
```

```blade
{{-- resources/views/components/post-card.blade.php --}}
<article @php post_class('post-card', $post) @endphp>
    @if(has_post_thumbnail($post))
        <div class="post-card__thumbnail">
            <a href="{!! get_permalink($post) !!}">
                {!! get_the_post_thumbnail($post, 'medium') !!}
            </a>
        </div>
    @endif
    
    <div class="post-card__content">
        <h3 class="post-card__title">
            <a href="{!! get_permalink($post) !!}">{!! get_the_title($post) !!}</a>
        </h3>
        
        @if($showMeta)
            <div class="post-card__meta">
                <span class="post-card__date">{!! get_the_date('', $post) !!}</span>
                <span class="post-card__author">{!! get_the_author_meta('display_name', $post->post_author) !!}</span>
            </div>
        @endif
        
        @if($showExcerpt)
            <div class="post-card__excerpt">
                {!! get_the_excerpt($post) !!}
            </div>
        @endif
    </div>
</article>
```

### Blade Directives

```php
// app/Providers/BladeServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Blade;

class BladeServiceProvider extends ServiceProvider {
    
    public function boot() {
        // Custom Blade directives
        Blade::directive('wpquery', function($expression) {
            return "<?php \$query = new WP_Query($expression); while(\$query->have_posts()): \$query->the_post(); ?>";
        });
        
        Blade::directive('endwpquery', function() {
            return "<?php endwhile; wp_reset_postdata(); ?>";
        });
        
        Blade::directive('acf', function($expression) {
            return "<?php echo get_field($expression); ?>";
        });
        
        Blade::directive('ifacf', function($expression) {
            return "<?php if(get_field($expression)): ?>";
        });
        
        Blade::directive('endifacf', function() {
            return "<?php endif; ?>";
        });
        
        Blade::directive('menu', function($expression) {
            return "<?php wp_nav_menu($expression); ?>";
        });
        
        Blade::directive('sidebar', function($expression) {
            return "<?php dynamic_sidebar($expression); ?>";
        });
    }
}
```

### Usage Examples

```blade
{{-- Using custom directives --}}
@wpquery(['post_type' => 'portfolio', 'posts_per_page' => 6])
    @include('components.portfolio-card')
@endwpquery

@ifacf('featured_content')
    <div class="featured-content">
        @acf('featured_content')
    </div>
@endifacf

@menu(['theme_location' => 'primary', 'container' => false])
@sidebar('primary-sidebar')
```

## Sage Services

### Service Container

```php
// app/Providers/ThemeServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Services\CustomService;
use App\Services\ApiService;

class ThemeServiceProvider extends ServiceProvider {
    
    public function register() {
        // Register services
        $this->app->singleton(CustomService::class, function($app) {
            return new CustomService();
        });
        
        $this->app->bind(ApiService::class, function($app) {
            return new ApiService($app->make(CustomService::class));
        });
    }
    
    public function boot() {
        // Boot services
        $this->app->make(CustomService::class)->boot();
    }
}
```

### Custom Services

```php
// app/Services/CustomService.php
namespace App\Services;

class CustomService {
    
    public function boot() {
        add_action('wp_enqueue_scripts', [$this, 'enqueueScripts']);
        add_action('wp_ajax_custom_action', [$this, 'handleAjax']);
        add_action('wp_ajax_nopriv_custom_action', [$this, 'handleAjax']);
    }
    
    public function enqueueScripts() {
        wp_enqueue_script('custom-script', get_template_directory_uri() . '/js/custom.js', ['jquery'], '1.0.0', true);
        wp_localize_script('custom-script', 'custom', [
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('custom_nonce'),
        ]);
    }
    
    public function handleAjax() {
        check_ajax_referer('custom_nonce', 'nonce');
        
        $data = $_POST['data'];
        $response = $this->processData($data);
        
        wp_send_json_success($response);
    }
    
    private function processData($data) {
        // Process data logic
        return ['processed' => true, 'data' => $data];
    }
}
```

## Asset Management

### Webpack Configuration

```javascript
// webpack.config.js
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = (env, argv) => {
    const isProduction = argv.mode === 'production';
    
    return {
        entry: {
            app: './resources/js/app.js',
            admin: './resources/js/admin.js',
        },
        
        output: {
            path: path.resolve(__dirname, 'dist'),
            filename: isProduction ? '[name].[contenthash].js' : '[name].js',
        },
        
        module: {
            rules: [
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env'],
                        },
                    },
                },
                {
                    test: /\.scss$/,
                    use: [
                        MiniCssExtractPlugin.loader,
                        'css-loader',
                        'postcss-loader',
                        'sass-loader',
                    ],
                },
                {
                    test: /\.(png|jpg|gif|svg)$/,
                    use: {
                        loader: 'file-loader',
                        options: {
                            name: isProduction ? '[name].[contenthash].[ext]' : '[name].[ext]',
                            outputPath: 'images/',
                        },
                    },
                },
            ],
        },
        
        plugins: [
            new CleanWebpackPlugin(),
            new MiniCssExtractPlugin({
                filename: isProduction ? '[name].[contenthash].css' : '[name].css',
            }),
        ],
        
        optimization: {
            splitChunks: {
                chunks: 'all',
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'vendors',
                        chunks: 'all',
                    },
                },
            },
        },
    };
};
```

### Asset Enqueuing

```php
// app/Providers/AssetServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use function Roots\bundle;

class AssetServiceProvider extends ServiceProvider {
    
    public function boot() {
        // Enqueue assets
        add_action('wp_enqueue_scripts', [$this, 'enqueueAssets']);
        add_action('admin_enqueue_scripts', [$this, 'enqueueAdminAssets']);
    }
    
    public function enqueueAssets() {
        // Enqueue main bundle
        bundle('app')->enqueue();
        
        // Conditional assets
        if (is_page_template('page-contact.php')) {
            bundle('contact')->enqueue();
        }
        
        if (is_singular('portfolio')) {
            bundle('portfolio')->enqueue();
        }
    }
    
    public function enqueueAdminAssets() {
        bundle('admin')->enqueue();
    }
}
```

## Sage with ACF

### ACF Integration

```php
// app/Providers/AcfServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class AcfServiceProvider extends ServiceProvider {
    
    public function boot() {
        if (!function_exists('acf_add_options_page')) {
            return;
        }
        
        // Add options pages
        acf_add_options_page([
            'page_title' => 'Theme Options',
            'menu_title' => 'Theme Options',
            'menu_slug' => 'theme-options',
            'capability' => 'edit_posts',
        ]);
        
        // Add sub pages
        acf_add_options_sub_page([
            'page_title' => 'Header Settings',
            'menu_title' => 'Header',
            'parent_slug' => 'theme-options',
        ]);
        
        acf_add_options_sub_page([
            'page_title' => 'Footer Settings',
            'menu_title' => 'Footer',
            'parent_slug' => 'theme-options',
        ]);
    }
}
```

### ACF Blade Helpers

```php
// app/Helpers/AcfHelper.php
namespace App\Helpers;

class AcfHelper {
    
    public static function field($field, $postId = null) {
        if (!function_exists('get_field')) {
            return null;
        }
        
        return get_field($field, $postId);
    }
    
    public static function option($field) {
        if (!function_exists('get_field')) {
            return null;
        }
        
        return get_field($field, 'option');
    }
    
    public static function hasField($field, $postId = null) {
        if (!function_exists('get_field')) {
            return false;
        }
        
        return !empty(get_field($field, $postId));
    }
}
```

```blade
{{-- Using ACF helpers in Blade --}}
@if(App\Helpers\AcfHelper::hasField('hero_image'))
    <div class="hero" style="background-image: url('{{ App\Helpers\AcfHelper::field('hero_image') }}')">
        <h1>{{ App\Helpers\AcfHelper::field('hero_title') }}</h1>
    </div>
@endif

<div class="site-footer">
    <p>&copy; {{ date('Y') }} {{ App\Helpers\AcfHelper::option('site_name') }}</p>
</div>
```

## Sage Best Practices

### Performance Optimization

```php
// app/Providers/PerformanceServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class PerformanceServiceProvider extends ServiceProvider {
    
    public function boot() {
        // Enable Blade caching in production
        if (!WP_DEBUG) {
            add_filter('blade/view/path', function($path) {
                return WP_CONTENT_DIR . '/cache/blade';
            });
        }
        
        // Optimize queries
        add_action('pre_get_posts', [$this, 'optimizeQueries']);
        
        // Cache expensive operations
        add_filter('blade/view/cache', function($cache) {
            return !WP_DEBUG;
        });
    }
    
    public function optimizeQueries($query) {
        if (is_admin() || !$query->is_main_query()) {
            return;
        }
        
        // Limit posts per page
        if (is_home() || is_archive()) {
            $query->set('posts_per_page', 10);
        }
        
        // Optimize search queries
        if (is_search()) {
            $query->set('posts_per_page', 8);
        }
    }
}
```

### Security Enhancements

```php
// app/Providers/SecurityServiceProvider.php
namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class SecurityServiceProvider extends ServiceProvider {
    
    public function boot() {
        // Remove WordPress version
        remove_action('wp_head', 'wp_generator');
        
        // Disable XML-RPC
        add_filter('xmlrpc_enabled', '__return_false');
        
        // Remove unnecessary headers
        remove_action('template_redirect', 'wp_shortlink_header', 11);
        
        // Security headers
        add_action('send_headers', [$this, 'addSecurityHeaders']);
        
        // Sanitize Blade output
        add_filter('blade/view/escape', [$this, 'escapeBladeOutput']);
    }
    
    public function addSecurityHeaders() {
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: SAMEORIGIN');
        header('X-XSS-Protection: 1; mode=block');
    }
    
    public function escapeBladeOutput($value) {
        return wp_kses_post($value);
    }
}
```

## Sage Examples

### Complete Theme Setup

```php
// app/Theme.php
namespace App;

use Illuminate\Container\Container;
use App\Providers\ThemeServiceProvider;
use App\Providers\AssetServiceProvider;
use App\Providers\BladeServiceProvider;

class Theme extends Container {
    
    public function __construct() {
        $this->registerProviders();
        $this->bootProviders();
    }
    
    private function registerProviders() {
        $providers = [
            ThemeServiceProvider::class,
            AssetServiceProvider::class,
            BladeServiceProvider::class,
        ];
        
        foreach ($providers as $provider) {
            $this->register(new $provider($this));
        }
    }
    
    private function bootProviders() {
        foreach ($this->getProviders() as $provider) {
            if (method_exists($provider, 'boot')) {
                $provider->boot();
            }
        }
    }
}

new Theme();
```

### Custom Post Type with Sage

```php
// app/PostTypes/Portfolio.php
namespace App\PostTypes;

use Illuminate\Support\ServiceProvider;

class Portfolio extends ServiceProvider {
    
    public function boot() {
        add_action('init', [$this, 'registerPostType']);
        add_action('init', [$this, 'registerTaxonomy']);
    }
    
    public function registerPostType() {
        register_post_type('portfolio', [
            'labels' => [
                'name' => 'Portfolio',
                'singular_name' => 'Portfolio Item',
                'add_new' => 'Add New Item',
                'add_new_item' => 'Add New Portfolio Item',
                'edit_item' => 'Edit Portfolio Item',
                'new_item' => 'New Portfolio Item',
                'view_item' => 'View Portfolio Item',
                'search_items' => 'Search Portfolio',
                'not_found' => 'No portfolio items found',
                'not_found_in_trash' => 'No portfolio items found in trash',
            ],
            'public' => true,
            'has_archive' => true,
            'supports' => ['title', 'editor', 'thumbnail', 'custom-fields'],
            'menu_icon' => 'dashicons-portfolio',
            'show_in_rest' => true,
        ]);
    }
    
    public function registerTaxonomy() {
        register_taxonomy('portfolio_category', 'portfolio', [
            'labels' => [
                'name' => 'Portfolio Categories',
                'singular_name' => 'Portfolio Category',
            ],
            'hierarchical' => true,
            'public' => true,
            'show_in_rest' => true,
        ]);
    }
}
```

## Official Documentation

https://roots.io/sage/
https://github.com/roots/sage
https://laravel.com/docs/9.x/blade
