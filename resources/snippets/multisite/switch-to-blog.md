---
difficulty: Advanced
tags: [multisite, network, sites, switching]
related: [multisite/network-settings]
use_case: Working with multiple sites
---

# Switch Between Sites

```php
// Get data from another site
function get_data_from_site( $blog_id ) {
    switch_to_blog( $blog_id );
    
    $posts = get_posts( array(
        'posts_per_page' => 10
    ));
    
    $site_name = get_bloginfo( 'name' );
    
    restore_current_blog();
    
    return array(
        'site_name' => $site_name,
        'posts' => $posts
    );
}

// Loop through all sites
function process_all_sites() {
    $sites = get_sites();
    
    foreach ( $sites as $site ) {
        switch_to_blog( $site->blog_id );
        
        // Do something on this site
        update_option( 'processed', true );
        
        restore_current_blog();
    }
}

// Get posts from all sites
function get_network_posts( $args = array() ) {
    $sites = get_sites();
    $all_posts = array();
    
    foreach ( $sites as $site ) {
        switch_to_blog( $site->blog_id );
        
        $posts = get_posts( $args );
        
        foreach ( $posts as $post ) {
            $post->site_id = $site->blog_id;
            $post->site_name = get_bloginfo( 'name' );
            $all_posts[] = $post;
        }
        
        restore_current_blog();
    }
    
    return $all_posts;
}
```
