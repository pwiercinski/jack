import tensorflow as tf


def train(loss, optim, batches, placeholders=None, predict=None, max_epochs=10,
          hooks=[], pre_run=None, post_run=None, sess=None):
    min_op = optim.minimize(loss)
    if sess is None:
        sess = tf.Session()

    with sess:
        tf.initialize_all_variables().run()

        for i in range(max_epochs):
            for j, batch in enumerate(batches):
                if placeholders is not None:
                    feed_dict = dict(zip(placeholders, batch))
                else:
                    feed_dict = batch

                if pre_run is not None:
                    pre_run(sess, i+1, feed_dict, loss, predict)

                _, current_loss = sess.run([min_op, loss], feed_dict=feed_dict)

                if post_run is not None:
                    post_run(sess, i+1, feed_dict, loss, predict)

                for hook in hooks:
                    hook(sess, i+1, predict, current_loss)

            # calling post-epoch hooks
            for hook in hooks:
                hook(sess, i+1, predict, 0)
