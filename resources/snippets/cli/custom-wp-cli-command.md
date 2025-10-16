---
difficulty: Advanced
tags: [cli, wp-cli, custom, commands]
related: [cli/wp-cli-commands]
use_case: Creating custom WP-CLI commands
---

# Custom WP-CLI Command

```php
// Register custom command
if ( defined( 'WP_CLI' ) && WP_CLI ) {
    WP_CLI::add_command( 'myplugin', 'MyPlugin_CLI_Commands' );
}

class MyPlugin_CLI_Commands {
    
    /**
     * Process all items
     *
     * ## OPTIONS
     *
     * [--limit=<number>]
     * : Number of items to process
     *
     * ## EXAMPLES
     *
     *     wp myplugin process --limit=100
     */
    public function process( $args, $assoc_args ) {
        $limit = isset( $assoc_args['limit'] ) ? intval( $assoc_args['limit'] ) : 10;
        
        WP_CLI::line( "Processing {$limit} items..." );
        
        $items = get_posts( array(
            'post_type' => 'my_cpt',
            'posts_per_page' => $limit
        ));
        
        $progress = \WP_CLI\Utils\make_progress_bar( 'Processing', count( $items ) );
        
        foreach ( $items as $item ) {
            // Process item
            do_something_with_item( $item );
            $progress->tick();
        }
        
        $progress->finish();
        
        WP_CLI::success( "Processed " . count( $items ) . " items!" );
    }
    
    /**
     * Export data to CSV
     *
     * ## EXAMPLES
     *
     *     wp myplugin export --file=export.csv
     */
    public function export( $args, $assoc_args ) {
        $filename = isset( $assoc_args['file'] ) ? $assoc_args['file'] : 'export.csv';
        
        $posts = get_posts( array( 'posts_per_page' => -1 ) );
        
        $fp = fopen( $filename, 'w' );
        fputcsv( $fp, array( 'ID', 'Title', 'Date' ) );
        
        foreach ( $posts as $post ) {
            fputcsv( $fp, array(
                $post->ID,
                $post->post_title,
                $post->post_date
            ));
        }
        
        fclose( $fp );
        
        WP_CLI::success( "Exported to {$filename}" );
    }
    
    /**
     * Clean up old data
     */
    public function cleanup() {
        $deleted = 0;
        
        // Delete old drafts
        $old_drafts = get_posts( array(
            'post_status' => 'draft',
            'date_query' => array(
                array( 'before' => '90 days ago' )
            ),
            'posts_per_page' => -1
        ));
        
        foreach ( $old_drafts as $draft ) {
            wp_delete_post( $draft->ID, true );
            $deleted++;
        }
        
        WP_CLI::success( "Deleted {$deleted} old drafts" );
    }
}
```
